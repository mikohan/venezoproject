$(document).ready(function(){
        var productForm = $('.form-product-ajax');

        productForm.submit(function(){
            event.preventDefault();
            var thisForm = $(this);
            var actionEndpoint = thisForm.attr('action');
            var httpMethod = thisForm.attr('method');
            var formData = thisForm.serialize();

            $.ajax({
                url: actionEndpoint,
                method: httpMethod,
                data: formData,
                success: function(data){
                    //console.log('success');
                    //console.log(data);
                    var submitSpan = thisForm.find('.submit-span');
                    if (data.added){
                        submitSpan.html('<button id="white_button2" type="submit">Убрать из корзины</button>');
                    } else {
                        submitSpan.html('<button id="white_button" type="submit">В корзину</button>');
                    }
                    var navbarCount = $('.navbar-cart-count');
                    var currentPath = window.location.href;
                    navbarCount.text(data.cartItemCount);
                    if (currentPath.indexOf('cart') != -1) {
                        refreshCart();
                    }
                },
                error: function(errorData){
                    console.log('error');
                    console.log(errorData);
                }
            });
        });


        function refreshCart(){
            var cartTable = $('.cart-table');
            var cartBody = cartTable.find('.cart-body');
            //cartBody.html('<h1>Changed</h1>');
            var productRows = cartBody.find('.cart-products');
            var currentUrl = window.location.href;
            var cartTotals = $('.cart-totals');

            var refreshCartUrl = '/api/cart/';
            var refreshCartMethod = 'GET';
            var data = {};
            $.ajax({
                url: refreshCartUrl,
                method: refreshCartMethod,
                data: data,
                success: function(data){

                    var hiddenCartItemRemoveForm = $(".cart-item-remove-form");

                    if (data.products.length > 0){
                        productRows.html('');
                        $.each(data.products, function(index, value){

                            var newCartItemRemove = hiddenCartItemRemoveForm.clone();
                            newCartItemRemove.css("display", "block");
                            newCartItemRemove.find(".cart-item-product-id").val(value.id);
                            cartBody.prepend('<tr><td>' + newCartItemRemove.html() + '</td><td class="product_thumb"><a href="/detailed2/' + value.id + '"><img src="/static/img/prod_thumbs/' + value.id + '.webp" alt=""></a></td><td class="product_name"><a href="/detail2/' + value.id + '/">' + value.name + '</a></td><td class="product-price">&#x20bd; ' + value.price + '</td><td class="product-price">&#x20bd; ' + value.price + '</td></tr>');
                        })
                        cartTotals.find('.cart-subtotal').text(data.subtotal);
                        cartTotals.find('.cart-total').text(data.total);
                    } else {
                        window.location.href = currentUrl;
                    }
                },
                error: function(errorData){
                    console.log(errorData);
                }
            });
        }

        // JS for add to cart on home page

        var productFormHome = $('.form-product-ajax-home');

        productFormHome.submit(function(){
            event.preventDefault();
            var thisForm = $(this);
            var actionEndpoint = thisForm.attr('action');
            var httpMethod = thisForm.attr('method');
            var formData = thisForm.serialize();

            $.ajax({
                url: actionEndpoint,
                method: httpMethod,
                data: formData,
                success: function(data){
                    //console.log('success');
                    //console.log(data);
                    var submitSpan = thisForm.find('.submit-span');
                    if (data.added){
                        submitSpan.html('<ul><li class="add_to_cart"><button type="submit" title="add to cart"><i class="ion-bag"></i> убрать</button></li><li class="wishlist"><a href="wishlist.html" title="Add to Wishlist"><i class="fa fa-heart-o"></i></a></li><li class="compare"><a href="#" title="compare"><i class="ion-ios-settings-strong"></i></a></li></ul>');
                    } else {
                        submitSpan.html('<ul><li class="add_to_cart"><button type="submit" title="add to cart" ><i class="ion-bag"></i> в корзину</button></li><li class="wishlist"><a href="wishlist.html" title="Add to Wishlist"><i class="fa fa-heart-o"></i></a></li><li class="compare"><a href="#" title="compare"><i class="ion-ios-settings-strong"></i></a></li></ul>');
                    }
                    var navbarCount = $('.navbar-cart-count');
                    var currentPath = window.location.href;
                    navbarCount.text(data.cartItemCount);
                    if (currentPath.indexOf('cart') != -1) {
                        refreshCart2();
                    }
                },
                error: function(errorData){
                    console.log('error');
                    console.log(errorData);
                }
            });
        });


        function refreshCart2(){
            var cartTable = $('.cart-table');
            var cartBody = cartTable.find('.cart-body');
            //cartBody.html('<h1>Changed</h1>');
            var productRows = cartBody.find('.cart-products');
            var currentUrl = window.location.href;
            var cartTotals = $('.cart-totals');

            var refreshCartUrl = '/api/cart/';
            var refreshCartMethod = 'GET';
            var data = {};
            $.ajax({
                url: refreshCartUrl,
                method: refreshCartMethod,
                data: data,
                success: function(data){

                    var hiddenCartItemRemoveForm = $(".cart-item-remove-form");

                    if (data.products.length > 0){
                        productRows.html('');
                        $.each(data.products, function(index, value){

                            var newCartItemRemove = hiddenCartItemRemoveForm.clone();
                            newCartItemRemove.css("display", "block");
                            newCartItemRemove.find(".cart-item-product-id").val(value.id);
                            cartBody.prepend('<tr><td>' + newCartItemRemove.html() + '</td><td class="product_thumb"><a href="/detailed2/' + value.id + '"><img src="" alt=""></a></td><td class="product_name"><a href="/detail2/' + value.id + '/">' + value.name + '</a></td><td class="product-price">&#x20bd; ' + value.price + '</td></tr>');
                        })
                        cartTotals.find('.cart-subtotal').text(data.subtotal);
                        cartTotals.find('.cart-total').text(data.total);
                    } else {
                        window.location.href = currentUrl;
                    }
                },
                error: function(errorData){
                    console.log(errorData);
                }
            });
        }

    });
