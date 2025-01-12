

// 表示データオブジェクト
var obj
// チェック用エリア
var check

async function check_write(check){

    let text = "let check_data = " + JSON.stringify(check)
    const blob = new Blob([text], {type: "text/plain"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "check.js";
    a.click();
    URL.revokeObjectURL(url);
    
}

// データ保存
function save(){
    data_save()
    //pythonでファイルに書き込み
    check_write(check)
}

function data_save(){
    //チェックボックスを確認し、チェックつきならデータを"get"に変更
    for(var i=0;i<obj["disp_data"].length;i++){
        let element = document.getElementById(obj["disp_data"][i].name)
        if(element.checked){
            check[obj["disp_data"][i].name] = "get"
        }else{
            check[obj["disp_data"][i].name] = ""
        }
    }
}

//2回目以降
function get_return_from_python(response) {
    obj = response["disp_data"]
    check = response["check"]
    //テーブル作成
    create_disp()

}

function get_return_from_python_first(response) {
    obj = response["disp_data"]
    check = response["check"]
    create_disp_first()
}

function ver_change(){
    data_save()
    let select = document.querySelector('[name="ver_select"]');
    object = {}
    object["disp_data"] = create_disp_data((select.selectedIndex)+1)
    object["check"] = check
    get_return_from_python(object)
}

//初回の表示作成
function create_disp_first(){
    //要素追加
    const select = document.createElement('select')
    select.name = "ver_select"
    select.id = "select"
    select.onchange = ver_change
    select.classList.add('select')
    
    obj["brand"].forEach((v) => {
        const option = document.createElement('option');
        option.value = v.value;
        option.textContent = v.name;
        select.appendChild(option);
      })
    
    const h2 = document.createElement('h2')
    h2.setAttribute("id","h2")

    let btn = document.createElement("button");
    btn.textContent = "データ保存";
    btn.setAttribute("onclick","save()")

    document.body.appendChild(select)
    document.body.appendChild(btn)

    document.body.appendChild(h2)


    
    select.selectedIndex = 0;

    //テーブル用要素
    const div = document.createElement("div")
    div.setAttribute("id","div1")
    document.body.appendChild(div)

    create_disp()

}

//スペシャルコーデ以外の時
function create_disp(){
    const h2 = document.getElementById('h2')
    document.getElementById('h2').textContent = obj.title
    // テーブルの要素をクリア
    const div_old = document.getElementById("div1")
    div_old.remove()
    div = document.createElement("div")
    div.setAttribute("id","div1")
    document.body.appendChild(div)

    //テーブル作成
    //該当箇所のアイテム数テーブルを作成
    for(var i=0;i<obj["disp_data"].length;i++){

        const table = document.createElement("table")
        table.border = 1
        table.style = "border-collapse: collapse"
        table.width = "500"

        //1テーブル生成1
        //tr(行)生成ループ
        for (var k=0;k<2;k++){
            //th(列)生成ループ
            var tr = document.createElement('tr')
            for (var l=0;l<2;l++){
                //1行目にコーデ名を入れる見出しを作成
                if(k==0 && l==0){
                    var th = document.createElement('th')
                    th.colSpan = 2
                    th.textContent = obj["disp_data"][i].name
                    tr.appendChild(th)
                }
                // フルコーデ画像を表示
                else if(k==1 && l==0){
                    var td = document.createElement('td')
                    td.rowSpan = 4
                    //画像パス 
                    var img = document.createElement("img")
                    img.src = obj["disp_data"][i].image
                    img.height = "180"
                    img.width = "160"
                    td.appendChild(img)
                    tr.appendChild(td)
                }
                else if(k==1 && l==1){
                    var td = document.createElement('td')
                    td.width = "400"
                    var ch = document.createElement('input');
                    ch.setAttribute('type','checkbox');
                    ch.setAttribute('name','name');

                    var label = document.createElement('label')

                    //トップス
                    ch.setAttribute('id',obj["disp_data"][i].name);
                    console.log(check[obj["disp_data"][i].name])
                    if (check[obj["disp_data"][i].name] == "get"){
                        ch.setAttribute('checked',ch[obj["disp_data"][i].name])
                    }
                    label.setAttribute("for",obj["disp_data"][i].name)
                    label.innerHTML = obj["disp_data"][i].name

                    td.appendChild(ch)
                    td.appendChild(label)
                    tr.appendChild(td)
                }
            }
            table.appendChild(tr)
        }

        div.appendChild(table)
    }
}

//JSから表示データの作成
function create_disp_data(brand){
    item_list = {}
    work = {}
    list = []

    brand_string = String(brand)
    item_list["select_brand"] = brand
    item_list["title"]=data["brand"][brand-1]["name"]
    item_list["brand"]=data["brand"]

    //全アイテムリストから該当ブランドのアイテムを順に抽出
    //for(i=0;i<9;i++){
    //    ver_string = String(i+1)
    //    for(i=0;i<item[ver_string].length;i++){
    //        work = {}
    //        if(item[ver_string][i]["brand"]==brand_string){
    //            work = Object.assign(work,item[ver_string][i])
    //            list.push(work)
    //        }
    //    }
    //}

    item_list["disp_data"] = item[brand_string]

    return item_list

}

function firstscript(){
    object={}
    object["disp_data"] = create_disp_data(1);
    object["check"] = check_data
    check_wk = check_data
    let div_element = document.getElementById("id1");
    div_element.remove()
    get_return_from_python_first(object)
}
