#数据校验

- 规则如下
  - 1、校验字段命名规则如：
    - 服务器返回字段
    ```json
    {
      "oldPassword": "abc123",
      "newPassword": "def456"
    }
    ```
    - 校验字段
    - 校验字段前加 assert_ 前缀
    - 校验 oldPassword 字段 没有的则不校验
    - assert_oldPassword 第一个值 & 判断必须有值；第二个值 str 判断当前类型；第二和第三值一起 判断当前值等于 abc123 
    
    ```json
    {
      "oldPassword": "",
      "assert_oldPassword":["?","str","=","abc123"], 
      "newPassword": "def456"
    }
    ```
   - 2、规则内容
     - 值1 
        - &  判断有值
        - ！ 判断无值
        - ？ 不做审核
     - 值2
        - str 字符类型
        - list 数组或者列表类型
        - dic 字段类型
        - bool 类型
        - int 类型
        - ? 类型不做判断
     - 值3
        - = 等于
        - \> 大于
        - \>= 大于等于
        - < 小于
        - <= 小于等于
        - <> 不等于
        - in 在其中
        - ? 值不做判断 
        - len.= 长度等于
        - len.> 长度大于
        - len.>= 长度大于等于
        - len.< 长度小于
        - len.<= 长度小于等于
        - len.<> 长度不等于
        - len.in 长度存在多个值中的一个
       
     - 值4 校验值
        
   - 3、列子
   
   ```json
    [
      {
        "method_name":"配置","api":"/dapi/common/config2","method":"get","description":"测试登录，吧啦吧啦吧啦，测试登录，吧啦吧啦吧啦",
        "assert":{
          "success": true,
          "assert_success": ["?","bool","<>",true],
          "data": {
            "students": [
              {
                "valid": true,
                "registered": true,
                "classId": "5c6e5bb276b2af4f0817ce48",
                "studentNumber": "20190112",
                "schoolName": "枞阳县白云中学",
                "authType": "formal",
                "packageType": "初中一年数理化家校版",
                "dueDate": "2019-02-28T00:00:00.000Z",
                "startYear": "2018",
                "schoolId": "5c6e47d9beb6431630d601ea",
                "stage": "senior",
                "mobile": "1550732329949",
                "realName": "李五柳",
                "registeredAt": "2019-03-06T07:19:56.789Z",
                "name": "devStu004",
                "id": "5c7e456a3bfb097f3c7f4472"
              }
            ]

          },
          "assert_data": ["!","dict","?",null]
      }},
      
      {"method_name":"配置","api":"/dapi/common/config","method":"get","description":"测试登录，吧啦吧啦吧啦，测试登录，吧啦吧啦吧啦"},
      {"method_name":"配置","api":"/dapi/common/config","method":"get","description":"测试登录，吧啦吧啦吧啦，测试登录，吧啦吧啦吧啦"},
      {"method_name":"配置","api":"/dapi/common/config","method":"get","description":"测试登录，吧啦吧啦吧啦，测试登录，吧啦吧啦吧啦"},
      {"method_name":"配置","api":"/dapi/common/config","method":"get","description":"测试登录，吧啦吧啦吧啦，测试登录，吧啦吧啦吧啦"},
      {"method_name":"配置","api":"/dapi/common/config","method":"get","description":"测试登录，吧啦吧啦吧啦，测试登录，吧啦吧啦吧啦"},
      {"method_name":"配置","api":"/dapi/common/config","method":"post","description":"测试登录，吧啦吧啦吧啦，测试登录，吧啦吧啦吧啦"}
    ]
    ```    
        
    