// Открытие окна просмотра
$("body").delegate("[data-do='open-view-position']", "click", function(){

	// Получаем информацию
	$.post("/tenders/ajax/get-plan-graph-position/", {
		position_id: $(this).data('id'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {
			if ('success' == data.status){

				// Заполняем значение полей
				$('#view-position-id').val(data.position['id']);
				$('#view-position-name').text(data.position['name']);

				$('#view-position-customer').data('id', data.position['customer']['id']);
				$('#view-position-customer').text(data.position['customer']['name']);

				$('#view-position-number').text(data.position['number']);
				$('#view-position-price').text(data.position['price']);

				okveds = ""
				for(i = 0; i < data.position.okveds.length; i++) {
					okved = data.position['okveds'][i].code + " " + data.position['okveds'][i]['name'] + "<br/>";
					okveds = okveds + okved;
				}
				$('#view-position-okveds').html(okveds);

				okpds = ""
				for(i = 0; i < data.position.okpds.length; i++) {
					okpd = data.position['okpds'][i].code + " " + data.position['okpds'][i]['name'] + "<br/>";
					okpds = okpds + okpd;
				}
				$('#view-position-okpds').html(okpds);

				if (data.position.products.length > 0) {

					products = '<table><tr><th>#</th><th>Наименование</th><th colspan="2">Количество</th><th>Цена</th><th>Сумма</th><th>ОКПД</th></tr>'

					for(i = 0; i < data.position.products.length; i++) {
						product = "<tr><td>" + data.position['products'][i].number + "</td><td>" + data.position['products'][i]['name'] + "</td><td>" + data.position['products'][i]['quantity'] + "</td><td>" + data.position['products'][i]['unit'] + "</td><td>" + data.position['products'][i]['price'] + "</td><td>" + data.position['products'][i]['max_sum'] + "</td><td>" + data.position['products'][i]['okpd'] + "</td></tr>";
						products = products + product;

					}
					products = products + "</table>"
					$('#view-position-products').html(products);
				}



				// Открываем окно
				$('#modal-view-plan-graph-position').foundation('reveal', 'open');

			} else {

				// Показываем сообщение с ошибкой
				var notification = new NotificationFx({
					wrapper : document.body,
					message : '<p>' + data.message + '</p>',
					layout : 'growl',
					effect : 'genie',
					type : data.status,
					ttl : 3000,
					onClose : function() { return false; },
					onOpen : function() { return false; }
				});
				notification.show();
			}
		}
	}, "json");

	return false;
});
