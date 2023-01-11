# Java-BOM-Analysis

## Overview

This repository contains `compare.py` which is a script designed to help perform analysis of existing Java projects built with Maven to review the dependancies listed in the applications Maven `pom.xml` and determine which if any of the dependancies are present in another `pom.xml`, and output the result in Markdown (the intersection of the two). This is useful for the circumstances in which you may be modifying the Maven build to include a Maven BOM (Bill of Materials) and want to determine which existing application dependancies may be made redundant/duplicative by dependancies provided by the BOM.

## BOM Anaylsis Example



## Credit

Thank you to esteemable kharyam (https://github.com/kharyam) for his initial work in this and assistance.
