---
title: "OCI Observability and Management - How to Publish Custom Metrics to OCI Monitoring Service "
date: 2023-04-17
last_modified_at: 2023-04-17T16:20:02-05:00
categories:
  - Blog
tags:
  - Observerability and Monitoring
---

### Introduction
With more and more customers embark journey to the Oracle Cloud, we see customers raise questions about Observability and Management best practices for Cloud Resources. OCI offers a range of tools and services for monitoring the health and performance of your cloud resources, including your databases, compute instances, network, application stack, etc. Highly scalable and resilient observability and monitoring solution is an essential part of any cloud deployment.

While OCI provides default metrics for some databases, there may be instances where custom metrics need to be used to monitor databases that are not monitored by default. Custom metrics allow you to monitor specific aspects of your databases that are critical to your business, but that are not captured by default metrics. For example, you may want to monitor the number of blocking sessions or long running sessions in your database, the response time of specific queries, or your Active Data Guard Transport and Apply lag. 

In this blog post, we will describe how to publish custom metrics to monitor databases that are not monitored by default by Oracle. We will explain how to create custom metrics using Oracle Management Cloud, a comprehensive monitoring solution that provides real-time visibility into your cloud resources, and how to publish these metrics in OCI. With custom metrics, you can gain deeper insights into the health and performance of your databases, detect issues early, and prevent downtime.

### Reference
Todd Sharp started with an awesome blog [Publishing and Analyzing Custom Applicatino Metrics with The Oracle Cloud Monitoring Service](https://blogs.oracle.com/developers/post/publishing-and-analyzing-custom-application-metrics-with-the-oracle-cloud-monitoring-service) with [Github code examples](https://github.com/recursivecodes/oci-custom-metrics) demonstrating how to create user defined custom metrics and publish them to user defined metric namespace in OCI Monitoring Service

read more about OCI Monitoring service [here](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Concepts/monitoringoverview.htm)


### Output

````
[opc@webinst01 libs]$ java -Dcom.sun.management.jmxremote -noverify ${JAVA_OPTS} -jar dbaas-metrics-0.1-all.jar
17:46:35.102 [main] INFO  i.m.context.env.DefaultEnvironment - Established active environments: [oraclecloud, cloud]
17:46:36.070 [main] INFO  com.zaxxer.hikari.HikariDataSource - HikariPool-1 - Starting...
17:46:36.074 [main] WARN  c.z.hikari.util.DriverDataSource - Registered driver with driverClassName=oracle.jdbc.driver.OracleDriver was not found, trying direct instantiation.
17:46:36.802 [main] INFO  com.zaxxer.hikari.HikariDataSource - HikariPool-1 - Start completed.
17:46:37.236 [pool-1-thread-1] INFO  com.oracle.bmc.Services - Registering new service: Services.BasicService(serviceName=AUTH, serviceEndpointPrefix=auth, serviceEndpointTemplate=null)
17:46:37.724 [pool-1-thread-1] INFO  c.o.b.a.AbstractFederationClientAuthenticationDetailsProviderBuilder - Looking up region for iad
17:46:37.729 [pool-1-thread-1] INFO  c.o.b.a.AbstractFederationClientAuthenticationDetailsProviderBuilder - Using region us-ashburn-1
17:46:37.730 [pool-1-thread-1] INFO  com.oracle.bmc.Region - Loaded service 'AUTH' endpoint mappings: {US_ASHBURN_1=https://auth.us-ashburn-1.oraclecloud.com}
17:46:37.731 [pool-1-thread-1] INFO  c.o.b.a.URLBasedX509CertificateSupplier - suppressX509Workaround flag set to false
17:46:38.223 [pool-1-thread-1] INFO  com.oracle.bmc.util.JavaRuntimeUtils - Determined JRE version as Unknown
17:46:38.224 [pool-1-thread-1] WARN  c.o.bmc.http.DefaultConfigurator - Using an unknown runtime, calls may not work
17:46:38.224 [pool-1-thread-1] INFO  c.o.bmc.http.DefaultConfigurator - Setting connector provider to HttpUrlConnectorProvider
17:46:38.281 [pool-1-thread-1] INFO  com.oracle.bmc.Services - Registering new service: Services.BasicService(serviceName=MONITORING, serviceEndpointPrefix=telemetry, serviceEndpointTemplate=https://telemetry.{region}.{secondLevelDomain})
17:46:38.284 [pool-1-thread-1] WARN  c.o.bmc.http.DefaultConfigurator - Using an unknown runtime, calls may not work
17:46:38.285 [pool-1-thread-1] INFO  c.o.bmc.http.DefaultConfigurator - Setting connector provider to HttpUrlConnectorProvider
17:46:38.291 [pool-1-thread-1] INFO  com.oracle.bmc.Region - Loaded service 'MONITORING' endpoint mappings: {US_ASHBURN_1=https://telemetry.us-ashburn-1.oraclecloud.com}
17:46:38.292 [pool-1-thread-1] INFO  c.o.bmc.monitoring.MonitoringClient - Setting endpoint to https://telemetry.us-ashburn-1.oraclecloud.com
17:46:38.292 [pool-1-thread-1] INFO  c.o.bmc.monitoring.MonitoringClient - Authentication details provider configured for region 'US_ASHBURN_1', but endpoint specifically set to 'https://telemetry-ingestion.us-phoenix-1.oraclecloud.com'. Using endpoint setting instead of region.
17:46:38.292 [pool-1-thread-1] INFO  c.o.bmc.monitoring.MonitoringClient - Setting endpoint to https://telemetry-ingestion.us-phoenix-1.oraclecloud.com
17:46:38.293 [pool-1-thread-1] INFO  c.recursive.job.MetricsPublisherJob - Publishing metrics...
17:46:38.303 [main] INFO  io.micronaut.runtime.Micronaut - Startup completed in 3308ms. Server Running: http://webinst01:8080
17:46:38.916 [pool-1-thread-1] INFO  c.o.b.a.i.X509FederationClient - Refreshing session keys.
17:46:39.054 [pool-1-thread-1] INFO  c.o.b.a.i.X509FederationClient - Getting security token from the auth server
17:46:39.170 [pool-1-thread-1] INFO  com.oracle.bmc.ClientRuntime - Using SDK: Oracle-JavaSDK/1.15.2
17:46:39.171 [pool-1-thread-1] INFO  com.oracle.bmc.ClientRuntime - User agent set to: Oracle-JavaSDK/1.15.2 (Linux/5.15.0-6.80.3.1.el8uek.x86_64; Java/11.0.18; Java HotSpot(TM) 64-Bit Server VM/11.0.18+9-LTS-195)
17:46:39.871 [pool-1-thread-1] ERROR i.m.s.DefaultTaskExceptionHandler - Error invoking scheduled task for bean [codes.recursive.job.MetricsPublisherJob@2ee4f54b] (404, NotAuthorizedOrNotFound, false) Authorization failed or requested resource not found. (opc-request-id: F7090AFA22504CF888B3DE59361AB8BD/342EC729DDED03A5DB664735BE56A374/AEF23A5999D5DB5652375CB042CA894D)
com.oracle.bmc.model.BmcException: (404, NotAuthorizedOrNotFound, false) Authorization failed or requested resource not found. (opc-request-id: F7090AFA22504CF888B3DE59361AB8BD/342EC729DDED03A5DB664735BE56A374/AEF23A5999D5DB5652375CB042CA894D)
	at com.oracle.bmc.http.internal.ResponseHelper.throwIfNotSuccessful(ResponseHelper.java:137)
	at com.oracle.bmc.http.internal.ResponseConversionFunctionFactory$ValidatingParseResponseFunction.apply(ResponseConversionFunctionFactory.java:87)
	at com.oracle.bmc.http.internal.ResponseConversionFunctionFactory$ValidatingParseResponseFunction.apply(ResponseConversionFunctionFactory.java:83)
	at com.oracle.bmc.monitoring.internal.http.PostMetricDataConverter$1.apply(PostMetricDataConverter.java:71)
	at com.oracle.bmc.monitoring.internal.http.PostMetricDataConverter$1.apply(PostMetricDataConverter.java:55)
	at com.oracle.bmc.monitoring.MonitoringClient.lambda$null$16(MonitoringClient.java:684)
	at com.oracle.bmc.retrier.BmcGenericRetrier.doFunctionCall(BmcGenericRetrier.java:87)
	at com.oracle.bmc.retrier.BmcGenericRetrier.lambda$execute$0(BmcGenericRetrier.java:58)
	at com.oracle.bmc.waiter.GenericWaiter.execute(GenericWaiter.java:54)
	at com.oracle.bmc.retrier.BmcGenericRetrier.execute(BmcGenericRetrier.java:49)
	at com.oracle.bmc.monitoring.MonitoringClient.lambda$postMetricData$17(MonitoringClient.java:676)
	at com.oracle.bmc.retrier.BmcGenericRetrier.doFunctionCall(BmcGenericRetrier.java:87)
	at com.oracle.bmc.retrier.BmcGenericRetrier.lambda$execute$0(BmcGenericRetrier.java:58)
	at com.oracle.bmc.waiter.GenericWaiter.execute(GenericWaiter.java:54)
	at com.oracle.bmc.retrier.BmcGenericRetrier.execute(BmcGenericRetrier.java:49)
	at com.oracle.bmc.monitoring.MonitoringClient.postMetricData(MonitoringClient.java:670)
	at codes.recursive.service.DBMetricsService.publishMetrics(DBMetricsService.java:107)
	at codes.recursive.job.MetricsPublisherJob.publishMetricsEverySixtySeconds(MetricsPublisherJob.java:24)
	at codes.recursive.job.$MetricsPublisherJobDefinition$$exec1.invokeInternal(Unknown Source)
	at io.micronaut.context.AbstractExecutableMethod.invoke(AbstractExecutableMethod.java:146)
	at io.micronaut.inject.DelegatingExecutableMethod.invoke(DelegatingExecutableMethod.java:76)
	at io.micronaut.scheduling.processor.ScheduledMethodProcessor.lambda$process$5(ScheduledMethodProcessor.java:120)
	at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:515)
	at java.base/java.util.concurrent.FutureTask.runAndReset(FutureTask.java:305)
	at java.base/java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:305)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
	at java.base/java.lang.Thread.run(Thread.java:834)
17:47:39.872 [pool-1-thread-3] INFO  c.recursive.job.MetricsPublisherJob - Publishing metrics...
17:47:40.556 [pool-1-thread-3] INFO  c.recursive.job.MetricsPublisherJob - Metrics published!
17:48:40.557 [pool-1-thread-2] INFO  c.recursive.job.MetricsPublisherJob - Publishing metrics...
17:48:41.175 [pool-1-thread-2] INFO  c.recursive.job.MetricsPublisherJob - Metrics published!
17:49:41.175 [pool-1-thread-3] INFO  c.recursive.job.MetricsPublisherJob - Publishing metrics...
17:49:41.804 [pool-1-thread-3] INFO  c.recursive.job.MetricsPublisherJob - Metrics published!
17:50:41.804 [pool-1-thread-2] INFO  c.recursive.job.MetricsPublisherJob - Publishing metrics...
17:50:42.577 [pool-1-thread-2] INFO  c.recursive.job.MetricsPublisherJob - Metrics published!
17:51:42.577 [pool-1-thread-3] INFO  c.recursive.job.MetricsPublisherJob - Publishing metrics...
17:51:43.300 [pool-1-thread-3] INFO  c.recursive.job.MetricsPublisherJob - Metrics published!
^C17:52:32.775 [Thread-2] INFO  io.micronaut.runtime.Micronaut - Embedded Application shutting down
17:52:33.090 [Thread-2] INFO  com.zaxxer.hikari.HikariDataSource - HikariPool-1 - Shutdown initiated...
17:52:33.187 [Thread-2] INFO  com.zaxxer.hikari.HikariDataSource - HikariPool-1 - Shutdown completed.
````

### Reference


