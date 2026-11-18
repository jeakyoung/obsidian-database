---
title: Quartz 기반 동적 스케줄 등록·해제 구조
date: 2026-11-18
type: 기술문서
project: SchedulerService
status: 완료
category: 스케줄링엔진
assignee:
  - 안재경
tags: []
---

# Quartz 기반 동적 스케줄 등록·해제 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | Scheduler-Service 백엔드 |
| **적용 범위** | 스케줄링 엔진 |
| **관련 모듈** | `QuartzConfig`, `GenericScheduleJob`, `ScheduleRegistrar`, `ScheduleBootstrapRunner` |

> 레거시의 "자바 코드에 Task 3개를 직접 등록"하는 방식을, Quartz JDBC JobStore 기반으로 DB에 저장된 스케줄 정의를 런타임에 동적으로 등록/해제하는 구조로 대체했다.

## 🎯 배경 및 요구사항

레거시 `SchedulerContextListener.contextInitialized()`는 `ScheduledExecutorService`에 `DaySchedulerTask`/`HourSchedulerTask`/`PurchaseReqSchedulerTask` 3개를 `scheduleAtFixedRate(initialDelay, period)`로 직접 등록했고, 각 Task 전용 메서드(`calculateInitialDelayForNextMonday9AM()` 등)로 "다음 실행까지 남은 초"를 계산했다. 스케줄을 바꾸려면 코드를 고치고 재배포해야 했다. 요구사항은 관리자 웹에서 스케줄을 Create/Update/Delete 하면 재시작 없이 즉시 반영되는 것.

## 🏗 설계 및 구현

### 구조

```
기동 시: ScheduleBootstrapRunner
  └─ schedule_definition에서 enabled=true 전체 조회
       └─ ScheduleRegistrar.register(definition) × N

관리자 API(생성/수정/삭제/토글)
  └─ ScheduleRegistrar.register/unregister
       └─ Quartz Scheduler.scheduleJob/rescheduleJob/deleteJob

Quartz 발화 시: GenericScheduleJob.execute()
  └─ JobDataMap에서 scheduleId만 꺼냄
       └─ 최신 ScheduleDefinition을 메타DB에서 재조회 (JobDataMap에 캐시 안 함)
            └─ ScheduleExecutor.execute(scheduleId, SCHEDULED)
```

- **스케줄 1개 = 범용 Job 1개**: 레거시가 Task 클래스 3개로 나눴던 걸, `GenericScheduleJob` 하나로 통합하고 SP명/cron/action_config는 모두 DB 행에서 읽는다.
- **Quartz가 Job을 직접 생성하는 문제**: Quartz는 리플렉션으로 Job 인스턴스를 직접 만들기 때문에 Spring 컨테이너를 거치지 않는다. `AutowiringSpringBeanJobFactory`(`SchedulerFactoryBeanCustomizer`로 등록) 없이는 `GenericScheduleJob`의 `@Autowired ScheduleExecutor`가 항상 null이 된다 — Spring Boot Quartz 자동구성이 기본 제공하지 않는 부분이라 직접 추가해야 했다.
- **Quartz cron은 Unix cron과 다르다**: day-of-month와 day-of-week 필드 중 하나는 반드시 `?`여야 한다(둘 다 `*`나 둘 다 구체값이면 무효). 테스트 cron(`"0 0 9 * * MON"`)이 전부 파싱 에러로 깨지는 걸 겪고서야 `"0 0 9 ? * MON"`으로 교정했다.
- **중복실행 가드**: 레거시의 `isTaskRunning`(static boolean, 클래스당 1개)을 Quartz `@DisallowConcurrentExecution`(스케줄 1개당 자동 격리)으로 대체. 수동실행(run-now)도 같은 `ScheduleExecutor` 경로를 타므로 "정규 실행 중 수동실행" 충돌도 같은 가드로 처리된다.

### 주요 로직

```java
// ScheduleRegistrar.register — 생성/수정/토글 전부 이 메서드 하나로
public void register(ScheduleDefinition definition) {
    unregister(definition.id()); // 멱등 — 기존 Job 먼저 제거
    if (!definition.enabled()) return; // 비활성이면 트리거 생성 안 함
    JobDetail job = JobBuilder.newJob(GenericScheduleJob.class)
        .withIdentity(jobKey(definition.id()))
        .usingJobData("scheduleId", definition.id())
        .build();
    Trigger trigger = TriggerBuilder.newTrigger()
        .forJob(job)
        .withSchedule(CronScheduleBuilder.cronSchedule(definition.cronExpression())
            .inTimeZone(TimeZone.getTimeZone(definition.timezone())))
        .build();
    scheduler.scheduleJob(job, trigger);
}
```

> [!note] 레거시 → 신규 매핑
> `calculateInitialDelayForNextMonday9AM()`/`calculateInitialDelayFor30Min()`/`calculateInitialDelayForDaily830AM()` 3종 전용 메서드가 전부 `CronTrigger` 하나로 대체됐다. 요일 조건(토/일 제외)도 cron 자체(`MON-FRI`)로 표현되어 런타임 분기 코드가 없어졌다.

## ✅ 검증

- [x] 기동 시 enabled 스케줄이 Quartz에 등록되고 다음 발화시각이 cron과 일치(통합테스트, `CronExpression.getNextValidTimeAfter`로 독립 계산한 값과 대조)
- [x] 활성/비활성 토글이 실제 Quartz 트리거 add/remove로 반영
- [x] cron 수정 시 재등록(cancel+재등록)이 실제로 다음발화시각을 바꿈
- [x] `AutowiringSpringBeanJobFactory` 없이는 `ScheduleExecutor`가 null이 되는 것을 실제로 재현 후 수정

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] 스케줄당 대상DB 다중 선택과 부분실패 처리]]
- `.team/LOG.md` T7 섹션 (Scheduler-Service 레포)
