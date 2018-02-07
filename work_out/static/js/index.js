
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
            new_name = prompt("请输入新建部位名称:","");
            if(new_name){
                res = self.post('/create_part', {'user_id': user_id, 'name': new_name});
            }
        }
        // 新建动作
        function create_item(part_id){
            new_name = prompt("请输入新建动作名称:","");
            if(new_name){
                res = self.post('/create_item', {'part_id': part_id, 'name': new_name})
            }
        }
        // 新建记录
        function create_record(item_id){
            weight = $('#weight').val();
            count = $('#count').val();
            if(!isNaN(weight) && !isNaN(count) && weight && count){
                res = self.post('/create_record', {'item_id': item_id, 'weight': weight, 'count': count});
            }
            else{$('#info').show()}
        }
        // 删除按钮
        function display(){
            $('.delete-action').show();
            $('#display').hide();
            $('#cancel').show();
        }
        function cancel(){
            $('.delete-action').hide();
            $('#cancel').hide();
            $('#display').show();
        }
        function spread(){
            $('.spread').show();
            $('#spread').hide();
            $('#roll').show();
        }
        function roll(){
            $('.spread').hide();
            $('#roll').hide();
            $('#spread').show();
        }

        $(document).ready(function(){
            $("#a_signup").click(function(){
                $('#login').hide();
            });
        });



        function find_record(day){
            date_input = $('#date_input').val();
            $.post('/find_record',{'date_str': date_input, 'day': day}, function(data){
                var obj = $.parseJSON(data).data;
                tbody = '';
                for(var i=0; i<obj.length; i++){
                    if (obj[i].records_list.length){
                        tbody += "<tr><td>"+ obj[i].name +"</td><td></td><td></td><td></td><td>"+obj[i].total+"</td></tr>";
                        records = obj[i].records_list;
                        for(var r=0; r<records.length; r++){
                            record = records[r];
                            tbody += "<tr style='display: none;' class='spread'><td></td><td>"+ record.item_name +"</td><td>"+ record.weight +"</td><td>"+ record.count +"</td><td>"+record.total+"</td></tr>";
                        }
                    }
                }
                tfoot = "<tr><td colspan='4'></td><td>"+ $.parseJSON(data).total +"</td></tr>";

                $('#tbody').html(tbody);
                $('#tfoot').html(tfoot);
                $('#date_input').val($.parseJSON(data).today);
            });
        };
        // 日期选择
        $(document).ready(function(){
            $(function(){
                $.post('/find_record',{'date_str': 'today'}, function(data){
                    var obj = $.parseJSON(data).data;
                    tbody = '';
                    for(var i=0; i<obj.length; i++){
                        if (obj[i].records_list.length){
                            tbody += "<tr><td>"+ obj[i].name +"</td><td></td><td></td><td></td><td>"+obj[i].total+"</td></tr>";
                            records = obj[i].records_list;
                            for(var r=0; r<records.length; r++){
                                record = records[r];
                                tbody += "<tr style='display: none;' class='spread'><td></td><td>"+ record.item_name +"</td><td>"+ record.weight +"</td><td>"+ record.count +"</td><td>"+record.total+"</td></tr>";
                            }
                        }
                    }
                    tfoot = "<tr><td colspan='4'></td><td>"+ $.parseJSON(data).total +"</td></tr>";

                    $('#tbody').html(tbody);
                    $('#tfoot').html(tfoot);
                    $('#date_input').val($.parseJSON(data).today);
                });
            });
            $("#date_input").blur(function(){
                date_input = $('#date_input').val();
                $.post('/find_record',{'date_str': date_input}, function(data){
                    var obj = $.parseJSON(data).data;
                    tbody = '';
                    for(var i=0; i<obj.length; i++){
                        if (obj[i].records_list.length){
                            tbody += "<tr><td>"+ obj[i].name +"</td><td></td><td></td><td></td><td>"+obj[i].total+"</td></tr>";
                            records = obj[i].records_list;
                            for(var r=0; r<records.length; r++){
                                record = records[r];
                                tbody += "<tr style='display: none;' class='spread'><td></td><td>"+ record.item_name +"</td><td>"+ record.weight +"</td><td>"+ record.count +"</td><td>"+record.total+"</td></tr>";
                            }
                        }
                    }
                    tfoot = "<tr><td colspan='4'></td><td>"+ $.parseJSON(data).total +"</td></tr>";

                    $('#tbody').html(tbody);
                    $('#tfoot').html(tfoot);
                    $('#date_input').val($.parseJSON(data).today);
                });
            });
        });