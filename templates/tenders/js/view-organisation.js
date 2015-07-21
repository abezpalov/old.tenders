// Открытие окна просмотра
$("body").delegate("[data-do='open-view-organisation']", "click", function(){

	// Получаем информацию
	$.post("/tenders/ajax/get-organisation/", {
		organisation_id: $(this).data('id'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {
			if ('success' == data.status){

				// Заполняем значение полей
				$('#view-organisation-id').val(data.organisation['id']);
				$('#view-organisation-full-name').text(data.organisation['full_name']);




				// Открываем окно
				$('#modal-view-organisation').foundation('reveal', 'open');

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
