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
				$('#edit-position-id').val(data.position['id']);
				$('#edit-position-name').text(data.position['name']);

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
