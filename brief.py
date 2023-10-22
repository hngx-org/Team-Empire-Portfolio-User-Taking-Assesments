title = "Assessment API"
summary="The API handles all Assessment related tasks for the HNGX  Zuri Portfolio Project  "
version="0.0.1"
docs="/api/v1"
description = """
### Summary

This version of the API can do awesome stuff like:

*Get All User Asessments*, *Start Assessment*, *Get Assessment Session Details*, *Get Assessment Result*,*Submit Assessment*,*Get User Completed Assessments*,*Get User Assessment*.

<details>
<summary>Brief Descriptions</summary>

### Get All User Asessments.  =>/assessments

```http
Method:GET
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. *header param* |


### Start Asessment.  =>/start-assessment

```http
Method:POST
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. *header param* |
| `assessment_id` | `dict` | **Required**. *request Body* |

### Get Assessment Session Details.  =>/session/assessment_id

```http
Method:GET
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. *header param* |
| `assessment_id` | `string` | **Required**. *path param* |

## Get Asessment Result.  =>/assessment_id/result

```http
Method:GET
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. *header param* |
| `assessment_id` | `string` | **Required**. *path param* |


### Submit Asessment.  =>/submit

```http
Method:POST
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. *header param* |
| `data` | `dict` | **Required**. *request Body* |


### Get User Completed Asessments.  =>/get-user-assessments

```http
Method:GET
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. *header param* |


### Get Asessment.  =>/skill_id

```http
Method:GET
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`      | `string` | **Required**. *header param* |
| `assessment_id` | `string` | **Required**. *path param* |

</details>



  
 
### Miscellaneous

How to generate token [Here](https://linear.app/zuri-project-backend/issue/TAK-15/get-user-assessment#comment-cdc22651)

---

"""