
        // js的post模拟表单提交方法
        function post(URL, PARAMS) {
            var temp = document.createElement("form");
            temp.action = URL;
            temp.method = "post";
            temp.style.display = "none";
            for (var x in PARAMS) {
            var opt = document.createElement("textarea");
            opt.name = x;
            opt.value = PARAMS[x];
            // alert(opt.name)
            temp.appendChild(opt);
            }
            document.body.appendChild(temp);
            temp.submit();
            return temp;
        }
        // 新建用户
        function create_user(){
            new_name = prompt("请输入你的姓名:","andy");
            age = prompt("请输入你的年龄:","20");
            gender = prompt("请输入你的性别:","男");
            res = self.post('/create_user', {'name': new_name, 'age': age, 'gender': gender})
        }
        // 新建部位
        function create_part(user_id){
            new_name = prompt("请输入新建部位名称:","背部");
            res = self.post('/create_part', {'user_id': user_id, 'name': new_name})
        }
        // 新建动作
        function create_item(part_id){
            new_name = prompt("请输入新建动作名称:","引体向上");
            res = self.post('/create_item', {'part_id': part_id, 'name': new_name})
        }
