 $(document).ready(function () {

            $("#btnShowModal").click(function () {

                $("#loginModal").modal('show');
            });

            $("#btnHideModal").click(function () {
                $("#loginModal").modal('hide');
            });

            $('#ok').click(function() {
   var amount=$("#amount").val();

   var date=$("#date").val();

   var category=$("#category").val();

   var desc=$("#desc").val();



   var formData = {'amount': amount, 'date' : date,'category': category, 'Description': desc};
    alert(formData);

        var res=$.ajax({
            type        : 'POST',
            url         : '/add_expense',
            data        : JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            dataType    : 'json',
            async: false
        }).responseText;

        alert(res);



    $("#loginModal").modal('hide');
});



});