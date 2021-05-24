// LocalStorageを使用してFormの状態を保持
$(function () {
    // Web Storageにフォームを保存
    $("form").submit(function () {
        // Key Valueでid, valueを格納
        let f = {};
        $("input,select").each(function () {
            f[$(this).attr("id")] = $(this).val();
        });
        
        // 辞書をJSON文字列化してWebStorageに保存
        localStorage.setItem("form", JSON.stringify(f));
    });
 
     // Web Storageからフォームを読込み
    function loadForm() {
        let f = JSON.parse(localStorage.getItem("form"));
        for (key in f)
            $("#" + key).val(f[key]);
    }
        
    // 前回の入力を読み込む
    loadForm();
    
});