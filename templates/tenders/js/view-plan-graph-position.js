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
					okved = "<p>" + data.position['okveds'][i].code + " " + data.position['okveds'][i]['name'] + "</p>";
					okveds = okveds + okved;
				}
				$('#view-position-okveds').html(okveds);

				okpds = ""
				for(i = 0; i < data.position.okpds.length; i++) {
					okpd = "<p>" + data.position['okpds'][i].code + " " + data.position['okpds'][i]['name'] + "</p>";
					okpds = okpds + okpd;
				}
				$('#view-position-okpds').html(okpds);


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
