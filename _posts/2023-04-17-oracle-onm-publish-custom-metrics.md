---
title: "OCI Observability and Management - How to Publish Custom Metrics to OCI Monitoring Service "
date: 2023-04-17
last_modified_at: 2023-04-17T16:20:02-05:00
categories:
  - Blog
tags:
  - Observability and Monitoring
---

### Introduction
With more and more customers embark journey to the Oracle Cloud, we see customers raise questions about Observability and Management best practices for Cloud Resources. OCI offers a range of tools and services for monitoring the health and performance of your cloud resources, including your databases, compute instances, network, application stack, etc. Highly scalable and resilient observability and monitoring solution is an essential part of any cloud deployment.

While OCI provides default metrics for some databases, there may be instances where custom metrics need to be used to monitor databases that are not monitored by default. **Custom metrics** allow you to monitor specific aspects of your databases that are critical to your business, but that are not captured by default metrics. For example, you may want to monitor the number of blocking sessions or long running sessions in your database, the response time of specific queries, or your Active Data Guard Transport and Apply lag. 

In this blog post, we will discuss how to deploy custom metrics to enrich Oracle database monitoring metrics in Oracle Cloud Infrastructure(OCI) which is not monitored by default. We will explain how to use OCI SDK to create custom metrics and how to publish these custom metrics to OCI O&M. With custom metrics, you can gain deeper insights into the health and performance of your databases, detect issues early, and prevent downtime.

### Reference
**Todd Sharp** started with an awesome blog [Publishing and Analyzing Custom Applicatino Metrics with The Oracle Cloud Monitoring Service](https://blogs.oracle.com/developers/post/publishing-and-analyzing-custom-application-metrics-with-the-oracle-cloud-monitoring-service) with [GitHub code example](https://github.com/recursivecodes/oci-custom-metrics) demonstrating how to create user defined custom metrics and publish them to user defined metric namespace in OCI Monitoring Service. This blog will focus on taking Todd's code into the OCI O&M environment and deploy the Java application into OCI Cloud. 

**Read more about OCI Monitoring service [here](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Concepts/monitoringoverview.htm)**

### Deployment Options
[OCI SDK and CLI](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/publishingcustommetrics.htm) provides very flexible development and deployment options for publishing custom metrics. Not only we can run the Java application in compute instance, we can also build the jar file and run the jar file directly within the cron job. Even we can use Fn project to deploy the java application into Oracle Functions. The implementation and deployment examples are no limited to above, for example, we can also use a shell script deployed in cronjob periodically connect to the database and run the SQL queries to check the long running session and spool the result into log file which subsequently stream log file into logging service and LA. Then we will create detection rule to publish the metrics pass the threshold into the monitoring service custom metric namespaces. 

We will discuss two options here: 
* **Run Java program locally in Inellij**
* **Build Jar file and schedule the jar file in the cronjob in compute instance**

**Todd** has pretty much all OCI database and compartments as well as API key related configurations mapped into following environment variables.

```bash
export DATASOURCES_DEFAULT_PASSWORD=[DBaaS password]
export DATASOURCES_DEFAULT_URL=[JDBC connect string]
export CODES_RECURSIVE_OCI_PROFILE=[For use when running locally - Default=DEFAULT]
export CODES_RECURSIVE_METRICS_NAMESPACE=[The namespace used to publish your custom metrics - whatever you want to use]
export CODES_RECURSIVE_USE_INSTANCE_PRINCIPAL=[Set to true when deployed on Oracle Cloud]
export CODES_RECURSIVE_METRICS_COMPARTMENT_OCID=[The compartment you want to publish your metrics in]
export CODES_RECURSIVE_DB_OCID=[Your DB OCID]
export DATASOURCES_DEFAULT_USERNAME=[DBaaS username]
export CODES_RECURSIVE_OCI_CONFIG_PATH=[The path to your local OCI config - Default=~/.oci/config]
```

**Note** : You need to have the API key to interact with the OCI services to publish custom metrics, to generate API key information, please follow this [Oracle Blog - Prep your Oracle Cloud tenancy for using SDKs](https://blogs.oracle.com/cloud-infrastructure/post/prep-your-oracle-cloud-tenancy-for-using-sdks)
### Run the Java program locally

After downloading Todd's GitHub code [repo](https://github.com/recursivecodes/oci-custom-metrics), you can open the folder in the [Intellij](https://www.jetbrains.com/help/idea/installation-guide.html).

**Prerequisits**

- User account which has the permission to manage metrics
- User account belongs to groups which have manage metrics permission for the compartment to publish custom metrics
- Database schema user account created for monitoring and retrieve database table or view data
- Database connection is accessible from local laptop environment to the database in OCI
- VCN subnet security list is updated to allow connection from local laptop

A few configuration changes are required before running the program locally

**Configure Environment Variables**

* Go to Intellij menu **Run**
* Select **Edit Configuration**
* Provide JDK environment and mainClass
* Provide Environment variables <img src='/images/posts/2023-04/royce-blog-2023-04-custom-metrics.png' alt='Environment variables'/>
* Run/Debug configurations page<img src='/images/posts/2023-04/royce-blog-2023-04-custom-metrics02.png' alt='Configuration'/>

**Update java file `src/main/java/service/DBMetricsService.java` with proper OCI Telemetry API endpoint before compile the code**

* If you monitoring service is running in US East Ashburn region, please update monitoringClient with correct api endpoint
* `monitoringClient = MonitoringClient.builder().endpoint("https://telemetry-ingestion.us-ashburn-1.oraclecloud.com").build(provider);`
* Example <img src='/images/posts/2023-04/royce-blog-2023-04-custom-metrics03.png'/>
* OCI API Reference: https://docs.oracle.com/en-us/iaas/api/#/en/monitoring/20180401/

**Update gradle build file `build.gradle` for the build**

* DriverClass `oracle.jdbc.OracleDriver` no longer works with the Java application, please update it to `com.oracle.database.jdbc` in `build.gradle` file
* Check following `compile group: 'com.oracle.database.jdbc', name: 'ojdbc8', version: '19.18.0.0'`
* Validate `build.gradle` file here 

```json
plugins {
id "net.ltgt.apt-eclipse" version "0.21"
id "com.github.johnrengelman.shadow" version "5.2.0"
id "application"
}

version "0.1"
group "codes.recursive"

repositories {
mavenCentral()
maven { url "https://jcenter.bintray.com" }
}

configurations {
// for dependencies that are needed for development only
developmentOnly 
}

dependencies {
annotationProcessor platform("io.micronaut:micronaut-bom:$micronautVersion")
annotationProcessor "io.micronaut:micronaut-inject-java"
annotationProcessor "io.micronaut:micronaut-validation"
implementation platform("io.micronaut:micronaut-bom:$micronautVersion")
implementation "io.micronaut:micronaut-inject"
implementation "io.micronaut:micronaut-validation"
implementation "io.micronaut:micronaut-runtime"
implementation "javax.annotation:javax.annotation-api"
implementation "io.micronaut:micronaut-http-server-netty"
implementation "io.micronaut:micronaut-http-client"
runtimeOnly "ch.qos.logback:logback-classic:1.2.3"
testAnnotationProcessor platform("io.micronaut:micronaut-bom:$micronautVersion")
testAnnotationProcessor "io.micronaut:micronaut-inject-java"
testImplementation platform("io.micronaut:micronaut-bom:$micronautVersion")
testImplementation "org.junit.jupiter:junit-jupiter-api"
testImplementation "io.micronaut.test:micronaut-test-junit5"
testRuntimeOnly "org.junit.jupiter:junit-jupiter-engine"

/* oci sdk */
compile 'com.oracle.oci.sdk:oci-java-sdk-full:1.15.2'
compile group: 'com.oracle.database.jdbc', name: 'ojdbc8', version: '19.18.0.0'
runtime 'io.micronaut.configuration:micronaut-jdbc-hikari'
compile 'com.sun.activation:jakarta.activation:1.2.1'
}

test.classpath += configurations.developmentOnly

mainClassName = "codes.recursive.Application"
// use JUnit 5 platform
test {
useJUnitPlatform()
}
tasks.withType(JavaCompile){
options.encoding = "UTF-8"
options.compilerArgs.add('-parameters')
}

shadowJar {
mergeServiceFiles()
}

run.classpath += configurations.developmentOnly
run.jvmArgs('-noverify', '-XX:TieredStopAtLevel=1', '-Dcom.sun.management.jmxremote')
```

**Run the application**

* Go to menu **Run**
* Select **Run 'Application'**
* See example output below <img src='/images/posts/2023-04/royce-blog-2023-04-custom-metrics04.png'/>

### Run the Java web application in compute instance

**Prerequisits**

- Create dynamic group for the compute instance
- Grant permissions to the dynamic group
- Dynamic group needs to have the permission to manage metrics
- Database schema user account created for monitoring and retrieve database table or view data
- Database connection is accessible from local laptop environment to the database in OCI
- VCN subnet security list is updated to allow connection from local laptop

The example code has option to be built the application using Gradle. You can follow the Intellij Gradle documentation - [Getting Started with Gradle](https://www.jetbrains.com/help/idea/getting-started-with-gradle.html). 

Once the local run is successful, we can use Gradle to build the Jar file and ready to deploy the jar file to compute instance. 

* Select Gradle window from the right natigation menu
* Expand build task
* Double-click build 
* <img src='/images/posts/2023-04/royce-blog-2023-04-custom-metrics05.png' width=500/>
* Build output <img src='/images/posts/2023-04/royce-blog-2023-04-custom-metrics06.png'/>
* You will find the `dbaas-metrics-0.1.jar` and `dbaas-metrics-0.1-all.jar` are generated in `build/libs` directory. 
* Next step is to copy the jar file `dbaas-metrics-0.1-all.jar` to the compute instance via `scp` command. 
* Once you have the jar file staged, it's ready to kick off the java application via `java -Dcom.sun.management.jmxremote -noverify ${JAVA_OPTS} -jar dbaas-metrics-0.1-all.jar` command. 
* <img src='/images/posts/2023-04/royce-blog-2023-04-custom-metrics07.png' width=500/>
* Congratulations! Now you will see your publish custom metrics application up and running in your compute instance. 

**Troubleshooting**: You may see exception about Authorization failure when publishing the metrics. The root cause is related to the compute instance instance principal dynamic group permission. You can read more about instance principal [here](https://docs.public.oneportal.content.oci.oraclecloud.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm)

```bash
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
```

**INSTANCE PRINCIPALS**
The IAM service feature that enables instances to be authorized actors (or principals) to perform actions on service resources. Each compute instance has its own identity, and it authenticates using the certificates that are added to it. These certificates are automatically created, assigned to instances and rotated, preventing the need for you to distribute credentials to your hosts and rotate them.

After updating the policies for the dynamic group of the compute instance to enable the capabilities of manage metrics in the compartment, the issue is fixed. 

**Example of required dynmaic groups and permissions**

```
ALL {instance.compartment.id='ocid1.compartment.oc1..aaaaaaaaexamplecompartmentocid'}
Allow dynamic-group obs-mgmt-compute-dg  to manage metrics in compartment obs_mgmt_comp
```

Example of the output running the jar file from the VM. 

```bash
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
```


