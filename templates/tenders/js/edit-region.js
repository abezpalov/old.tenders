{% if perms.tenders.change_region %}


// Открытие окна редактирования
$("body").delegate("[data-do='open-edit-region']", "click", function(){

	// Получаем информацию о загрузчике
	$.post("/tenders/ajax/get-region/", {
		region_id: $(this).data('id'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {
			if ('success' == data.status){

				// Заполняем значение полей
				$('#edit-region-id').val(data.region['id']);
				$('#edit-region-name').val(data.region'name']);
				$('#edit-region-full-name').val(data.region['full_name']);
				$('#edit-region-alias').val(data.region['alias']);
				$('#edit-region-country').val(data.region['counry']);
				$('#edit-region-state').prop('checked', data.region['state']);

				// Открываем окно
				$('#modal-edit-region').foundation('reveal', 'open');

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


// Сохранение
$("body").delegate("[data-do='edit-region-save']", "click", function(){

	// Отправляем запрос
	$.post("/tenders/ajax/save-region/", {
		region_id:           $('#edit-region-id').val(),
		region_name:         $('#edit-region-name').val(),
		region_full_name:    $('#edit-region-full-name').val(),
		region_alias:        $('#edit-region-alias').val(),
		region_country:      $('#edit-region-country').val(),
		region_state:        $('#edit-region-state').prop('checked'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {

			// Показываем сообщение
			var notification = new NotificationFx({
				wrapper: document.body,
				message: '<p>' + data.message + '</p>',
				layout:  'growl',
				effect:  'genie',
				type:    data.status,
				ttl:     3000,
				onClose: function() { return false; },
				onOpen:  function() { return false; }
			});
			notification.show();

			if ('success' == data.status){

				// Обновлем информацию на странице
				$("[data-region-name='" + $('#edit-region-id').val() + "']").text($('#edit-region-name').val());
				$("[data-region-state='" + $('#edit-region-id').val() + "']").prop('checked', $('#edit-region-state').prop('checked'));
				// TODO обновление стран

				// Заполняем значение полей
				$('#edit-region-id').val('0');
				$('#edit-region-name').val('');
				$('#edit-region-full-name').val('');
				$('#edit-region-alias').val('');
				$('#edit-region-country').val('');
				$('#edit-region-state').prop('checked', false);

				// Закрываем окно
				$('#modal-edit-region').foundation('reveal', 'close');
			}
		}
	}, "json");

	return false;
});


// Отмена редактирования загрузчика
$("body").delegate("[data-do*='edit-region-cancel']", "click", function(){

	// Заполняем значение полей
	$('#edit-region-id').val('0');
	$('#edit-region-name').val('');
	$('#edit-region-full-name').val('');
	$('#edit-region-alias').val('');
	$('#edit-region-country').val('');
	$('#edit-region-state').prop('checked', false);

	// Закрываем окно
	$('#modal-edit-region').foundation('reveal', 'close');

	return false;
});

{% endif %}

{% if perms.tenders.change_region %}


// Смена статуса
$("body").delegate("[data-do='switch-region-state']", "click", function(){

	// Отправляем запрос
	$.post("/tenders/ajax/switch-region-state/", {
		region_id:           $(this).data('id'),
		region_state:        $(this).prop('checked'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {

			// Показываем сообщение
			var notification = new NotificationFx({
				wrapper: document.body,
				message: '<p>' + data.message + '</p>',
				layout:  'growl',
				effect:  'genie',
				type:    data.status,
				ttl:     3000,
				onClose: function() { return false; },
				onOpen:  function() { return false; }
			});
			notification.show();

			// Проверем успешность запроса
			if ('success' != data.status){
				setTimeout(function () {location.reload();}, 3000);
			}
		}
	}, "json");

	return true;
});

{% endif %}
