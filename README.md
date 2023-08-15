# BDP

## cluster stack

| stack             | version     |
|:------------------|:------------|
| hadoop            | 3.2.3       |
| tez               | 0.10.1      |
| hive              | 3.1.3       |
| hbase             | N/A         |
| zookeeper         | 3.6.3       |
| spark             | 3.3.0       |
| kafka             | 3.2.0       |
| debezium          | 1.5.4       |
| airflow           | 2.2.5       |
| mysql             | 8.0.30      |
| hue               | N/A         |
| zeppelin          | 0.10.1      |
| java              | openjdk-1.8 |
| python            | 3.10.0      |
| scala             | 2.13.8      |


<br/>

## 사전 준비

### 1. VM 생성

vagrant-scripts 디렉토리를 VM을 생성시킬 리눅스 장비의 특정경로에 위치시키고,

vagrant-scripts 하위에 `node-specs.yml`을 정의하여 생성할 VM별 스펙을 명시합니다.
이후, vagrant-scripts 경로에서 아래 명령을 실행하여 VM을 생성합니다.

```bash
>> 'VAGRANT_EXPERIMENTAL="disks" vagrant up'
```

<details>
<summary>node-specs.yml 예시</summary>
  
```yaml
- name: bdp-dn1
  box: rockylinux/8
  network: public_network
  network_if: enp1s0
  ip: 192.168.45.241
  mem: 16
  cpu: 4
  disk: 100
  items:
    - install-python

- name: bdp-dn2
  box: rockylinux/8
  network: public_network
  network_if: enp1s0
  ip: 192.168.45.242
  mem: 16
  cpu: 4
  disk: 100
  items:
    - install-python

- name: bdp-dn3
  box: rockylinux/8
  network: public_network
  network_if: enp1s0
  ip: 192.168.45.243
  mem: 16
  cpu: 4
  disk: 100
  items:
    - install-python

- name: bdp-nn2
  box: rockylinux/8
  network: public_network
  network_if: enp1s0
  ip: 192.168.45.245
  mem: 20
  cpu: 4
  disk: 100
  items:
    - install-python

- name: bdp-nn1
  box: rockylinux/8
  network: public_network
  network_if: enp1s0
  ip: 192.168.45.240
  mem: 20
  cpu: 4
  disk: 100
  items:
    - install-python

- name: bdp-eg1
  box: rockylinux/8
  network: public_network
  network_if: enp1s0
  ip: 192.168.45.244
  mem: 20
  cpu: 8
  disk: 200
  items:
    - install-python
    - setup-ansible
    - copy-sshkey
```
</details>

<br/>

### 2. ansible 준비

ansible-hadoop 디렉토리를 `setup-ansible`을 수행한 VM의 root 경로에 위치시킵니다.

이후, `inventories/host.yml` 파일에 각 컴포넌트를 어떤 VM에 위치시킬지를 정의합니다.

<details>
<summary>host.yml 예시</summary>

```yaml
all:
  hosts:
    bdp-nn[1:2]:
    bdp-eg1:
    bdp-dn[1:3]:
  
  children:
    appmaster:
      hosts:
        bdp-eg1:

    namenode:
      hosts:
        bdp-nn1:
          status: active
        bdp-nn2:
          status: standby
    
    datanode:
      hosts:
        bdp-dn[1:3]:

    resourcemanager:
      hosts:
        bdp-nn[1:2]:

    journalnode:
      hosts:
        bdp-eg1:
        bdp-nn[1:2]:

    historyserver:
      hosts:
        bdp-nn2:

    zookeeper:
      hosts:
        bdp-eg1:
          id: 1
        bdp-nn1:
          id: 2
        bdp-nn2:
          id: 3

    kafka:
      hosts:
        bdp-dn1:
          id: 1
        bdp-dn2:
          id: 2
        bdp-dn3:
          id: 3

    kafka_connect:
      hosts:
        bdp-eg1:

    mysql:
      hosts:
        bdp-nn1:

    airflow:
      hosts:
        bdp-eg1:

    hiveserver2:
      hosts:
        bdp-nn1:

    hivemetastore:
      hosts:
        bdp-nn1:

    spark_historyserver:
      hosts:
        bdp-nn2:

    zeppelin:
      hosts:
        bdp-eg1:

    hadoop:
      children:
        namenode:
        datanode:
        resourcemanager:
        journalnode:
        historyserver:

    hive:
      children:
        hiveserver2:
        hivemetastore:

    spark:
      children:
        spark_historyserver:
```
</details>

<br/>

## 실행

클러스터를 구성하는 각 컴포넌트별로 선후행 디펜던시를 가지고 있기에 

```bash
>> python ansible-hadoop/cluster-py/cluster.py all start
```