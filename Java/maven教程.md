# maven教程.md
---

## maven 介绍
Apache maven, 是一个软件(特别是Java软件)项目管理以及自动构建工具, 有apache软件基金会所提供. 基于项目对象模型(缩写:POM)概念, Maven利用一个中央信息片段能管理一个项目构建, 报告和文档等步骤.
Maven也可以被用于构建和项目管理项目, 如C#, Ruby等.

## 安装
### windows
- 1.下载 apache-maven-3.3.9-bin.zip
- 2.在相应的目录下解压软件
- 3.添加maven 的路径到环境变量path(C:\Program Files\apache-maven-3.3.9\bin)
- 4.设置好JAVA_HOME

## maven的配置文件


## pom.xml文件

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
   http://maven.apache.org/xsd/maven-4.0.0.xsd">
   <modelVersion>4.0.0</modelVersion>

   <groupId>com.companyname.project-group</groupId>
   <artifactId>project</artifactId>
   <version>1.0</version>

</project>
```
1. 所有的POM文件需要project元素和三个必须的字段: groupId, artifactId, version.
2. 在仓库中的工程标识为groupId:artifactId:version
3. POM.xml的根元素是project, 它主要有三个主要的子节点:
  1. groupId: 这是工程组的标识, 他在一个组织或者一个项目中通常是唯一的. 例如, 一个银行组织com.company.bank拥有所有的和银行相关的项目.
  2. artfactId: 这是工程的标识. 他通常是工程的名称. 例如, 消费银行. groupId和artfactId一起定义了artifact在仓库中的位置.
  3. version: 这是工程版本号. 在artifactId的仓库中, 它用来区分不同的版本. 例如:com.company.bank:comsumer-banking:1.0 com.compayn.bank.comsumer-banking:1.1

实例:
```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.htop</groupId>
  <artifactId>springmvcdemo</artifactId>
  <packaging>war</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>springmvcdemo Maven Webapp</name>
  <url>http://maven.apache.org</url>
  <!--<properties>-->
    <!--<spring.version>4.3.3.RELEASE</spring.version>-->
  <!--</properties>-->
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
    <!-- https://mvnrepository.com/artifact/org.springframework/spring-core -->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>4.2.8.RELEASE</version>
    </dependency>
    <!-- https://mvnrepository.com/artifact/org.springframework/spring-context -->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>4.2.8.RELEASE</version>
    </dependency>

      <dependency>
          <groupId>org.springframework</groupId>
          <artifactId>spring-web</artifactId>
          <version>4.2.8.RELEASE</version>
      </dependency>

      <!-- https://mvnrepository.com/artifact/org.springframework/spring-webmvc -->
      <dependency>
          <groupId>org.springframework</groupId>
          <artifactId>spring-webmvc</artifactId>
          <version>4.2.8.RELEASE</version>
      </dependency>


      <dependency>
          <groupId>javax.servlet</groupId>
          <artifactId>jstl</artifactId>
          <version>1.2</version>
      </dependency>

    <!--<dependency>-->
      <!--<groupId>mysql</groupId>-->
      <!--<artifactId>mysql-connector-java</artifactId>-->
    <!--</dependency>-->
  </dependencies>
  <build>
    <finalName>springmvcdemo</finalName>
  </build>
</project>

```

## IDEA 通过maven建立springmvc和mybatis工程

new project --> maven --> org.apache.maven.archetypes:maven-archtype-webapp
 
