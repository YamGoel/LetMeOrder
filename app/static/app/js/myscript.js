$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity
            document.getElementById("amount").innerText = "Rs. "+data.amount
            var parcelamount = document.getElementById("parcel_amount").innerText
            var p = parseInt(parcelamount)
            document.getElementById("totalamount").innerText =  data.totalamount+p
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity
            document.getElementById("amount").innerText = "Rs. "+data.amount
            var parcelamount = document.getElementById("parcel_amount").innerText
            var p = parseInt(parcelamount)
            document.getElementById("totalamount").innerText =  data.totalamount+p
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText = "Rs. "+data.amount
            var parcelamount = document.getElementById("parcel_amount").innerText
            var p = parseInt(parcelamount)
            document.getElementById("totalamount").innerText =  data.totalamount+p
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

$('.order-completed').click(function(){
    var id = $(this).attr("oid").toString()
    var eml = this
    $.ajax({
        type:"GET",
        url:"/ordercompleted",
        data:{
            orderid:id
        },
        success:function(data){
            var sid = data.storeid
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})