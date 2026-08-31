
.\build.bat dev
.\build.bat prod

유동적 커넥션 사용을 위해 빌드방식을 build.bat에 정의해두었음

빌드완료후 -> ssh f1soft@192.168.80.27 서버접근


scp WEB-INF/classes/com/scheduler/*.class \                                                                                                                           
    f1soft@192.168.80.27:/home/f1soft/groupware/groupware_cls/com/scheduler/


~/groupware/groupware_cls/com/scheduler 내에 클래스 업로드

standalone Java 프로세스로 시행중임

cd /home/f1soft/groupware/groupware_cls -> 클래스 경로로 이동해서

ps -ef | grep java

찾아서 기존 프로세스 끄고

java -cp .:./../lib/* com.scheduler.SchedulerContextListener &

정의해둔 메인클래스로 재시행


현 상태 : PROD로 빌드해놓고 클래스 배포만 하면됨

218.155.74.4


scp -r "C:/Users/USER/Desktop/scheduler-test/scheduler-test/out/production/scheduler-test/com/scheduler" f1soft@192.168.80.27:/home/f1soft/groupware/groupware_cls/com/

cd /home/f1soft/groupware/groupware_cls                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
nohup java -cp .:./lib/* com.scheduler.SchedulerContextListener > /dev/null 2>&1 &

ps -ef | grep SchedulerContextListener

