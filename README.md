# lina_anonymizer
text anonymizer based on flow

## overall workflow
```mermaid
graph TD;
    AA[annotator] --> |register rule-set|A
    A[strapi]-->|get regex|B[rule-entity-extractor server];
    B --> |return matched result|C[node-red flow];
    C --> |match regex|B;
    Q[query text from user] --> C;
    C --> |masking personal information|D[anonymized text];
```

## Architecture(As-is)
```mermaid
graph TD;
    A[strapi - EC2] --> B[rule-entity-extractor - EC2];
    B --> C[node-red - EC2];
    D[User query] --> C;
    C --> E[masked result];
```

## Architecture(To-be)
```mermaid
graph TD;
    A[k8s] --> B[pod1]
    A[k8s] --> C[pod2]
    A[k8s] --> D[pod3]
    B --> E[strapi docker]
    C --> F[node-red docker]
    D --> G[rule server docker]
    E --> F
    F --> G
```

## To-do
- 현업들과의 미팅을 통한 온톨로지 구축
- 쉬운 정규식 generator 가능?
- 회사 관점에서의 결과값(로그)를 통한 메트릭 추출이 가능?
- 실시간 inference 환경에서는 고객 정보 실시간 업데이트 가능(엔티티 제대로 추출할 경우)!
- 
