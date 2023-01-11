# Java-BOM-Analysis

## Overview

This repository contains `compare.py` which is a script designed to help perform analysis of existing Java projects built with Maven to review the dependencies listed in the applications Maven `pom.xml` and determine which if any of the dependencies are present in another `pom.xml`, and output the result in Markdown (the intersection of the two). This is useful for the circumstances in which you may be modifying the Maven build to include a Maven BOM (Bill of Materials) and want to determine which existing application dependencies may be made redundant/duplicative by dependencies provided by the BOM.

## BOM Analysis Example

This script was created to assist with analysis of a portfolio of Java applications, reviewing the dependencies declared in the applications Maven `pom.xml` and determining quickly what dependencies would be duplicated with the inclusion of a BOM, in this case, the Red Hat `org.jboss.bom | jboss-eap-jakartaee8-with-tools | 7.4.0.GA` BOM.

In order to demonstrate the use of this, a example directory has been created in this project, containing the following:

```
$ ls -1 ./example/
pom-empty-with-bom.xml
pom-my-app.xml
```

* `pom-my-app.xml` is a example `pom.xml` for my application that declares a few dependencies that I happen to know are also declared in the aforementioned BOM.
* `pom-empty-with-bom.xml` is a standard empty template `pom.xml` file declares a dependency on the Red Hat `org.jboss.bom | jboss-eap-jakartaee8-with-tools | 7.4.0.GA` BOM.

The following Maven command is run against our `pom-empty-with-bom.xml`, to generate the effective-pom that explicitly lists all the dependencies provided by the BOM.

```
mvn help:effective-pom -f ./example/pom-empty-with-bom.xml -Doutput=./effective-pom.xml
```

Once we have our effective pom, we can run the compare script to see what our app dependencies are also in the the effective pom, representing all dependencies provided by our bom.

```
$ ./compare.py --template=./example/effective-pom.xml --pom=./example/pom-my-app.xml
| groupId | artifactId | pom.xml version | BOM version |
|---|---|---|---|
| org.hibernate | hibernate-envers | 5.1.17.Final | 5.3.20.Final-redhat-00001 |
| org.hibernate | hibernate-entitymanager | 5.1.17.Final | 5.3.20.Final-redhat-00001 |
```

And of course this output renders as a nice markdown table:

| groupId | artifactId | pom.xml version | BOM version |
|---|---|---|---|
| org.hibernate | hibernate-envers | 5.1.17.Final | 5.3.20.Final-redhat-00001 |
| org.hibernate | hibernate-entitymanager | 5.1.17.Final | 5.3.20.Final-redhat-00001 |

## Credit

Thank you to esteemable kharyam (https://github.com/kharyam) for his initial work in this and assistance.
