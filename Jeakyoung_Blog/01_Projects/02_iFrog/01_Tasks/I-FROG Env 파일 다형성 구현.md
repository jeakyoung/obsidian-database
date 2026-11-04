---
title: I-FROG Env 파일 다형성 구현
date: 2026-06-10
type: 작업
project: I-Frog
status: 완료
priority: 보통
assignee: []
tags: []
created: 2026-06-10T14:29:00
---

# I-FROG Env 파일 다형성 구현

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-10 |
| **대상 시스템** | — |
| **관련 화면·프로그램** | — |

## 🔍 현상 및 원인

## 🔧 조치 내용

### 인터페이스를 사용한 다중 상속 구현하기

다중 상속은 클래스 하나를 콤마로 구분해서 인터페이스 하나 이상을 상속하는 것을 의미합니다. C#에서 클래스는 클래스에 대한 단일 상속만 지원하는 대신, 인터페이스는 클래스에 인터페이스를 하나 이상 상속할 수 있습니다. 다음 내용을 입력한 후 실행해 보세요.

인터페이스를 사용한 다중 상속: InterfaceInheritance.cs

`using System;

namespace InterfaceInheritance
{
    interface IAnimal
    {
        void Eat();
    }

    interface IDog
    {
        void Yelp();
    }

    class Dog : IAnimal, IDog //인터페이스를 사용한 다중 상속
    {
        public void Eat() => Console.WriteLine("먹다.");
        public void Yelp() => Console.WriteLine("짖다.");
    }

    class InterfaceInheritance
    {
        static void Main()
        {
            Dog dog = new Dog();
            dog.Eat();     //ⓐ IAnimal 인터페이스 상속
            dog.Yelp();    //ⓑ IDog 인터페이스 상속
        }
    }
}`

```plain text
실행 결과
먹다.
짖다.
```

Dog 클래스는 IAnimal 인터페이스와 IDog 인터페이스에서 다중 상속을 받습니다. IAnimal 인터페이스에서 Eat() 메서드를 상속받고 IDog 인터페이스에서 Yelp() 메서드를 상속받아 메서드 2개의 내용을 Dog 클래스에서 직접 구현하는 형태입니다.


기존방식

- 헤더로 보안 코드를 가져와서 회사이름, db커넥션 정보를 매퍼로 만든다
- 그걸로 DB 커넥션을 생성하고
- 서비스를통해 개별 DB에 저장되어 있는 도메인값을 가져온다.

## ✅ 검증 및 결과

## 🔗 참고
