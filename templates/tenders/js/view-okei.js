// Поиск по справочнику
$("body").delegate("[data-do='okeis-search']", "keypress", function(e){
	var search_text = $(this).val().toLowerCase();
	var key         = e.which;

	if(key == 13) {

		// Если в строке поиска пусто, показываем полный каталог
		if (search_text == '') {
			$("[data-content='okeis-search-result']").addClass('hidden');
			$("[data-content='okeis-catalog']").removeClass('hidden');
			$("[data-content='okeis-search-result']").html('');
		// Иначе, прячем каталог и показываем результаты поиска
		} else {
			$("[data-content='okeis-search-result']").removeClass('hidden');
			$("[data-content='okeis-catalog']").addClass('hidden');

			// Получаем объекты с сервера
			$.post("/tenders/ajax/search-okeis/", {
				search_text:         search_text,
				csrfmiddlewaretoken: '{{ csrf_token }}'
			},
			function(data) {
				if (null != data.status) {

					if ('success' == data.status){

						html_data = ""

						if (data.okeis.length > 0) {
							for(i = 0; i < data.okeis.length; i++) {
								li = '<li><a data-do="open-view-okei" data-id="' + data.okeis[i]['id'] + '"><span>' + data.okeis[i]['full_name'] + '</span>'
								if (data.okeis[i]['local_name']) {
									li = li + '<span>(' + data.okeis[i]['local_name'] + ')</span>'
								}
								li = li + '</a></li>'
								html_data = html_data + li;
							}
						} else {
							html_data = '<li class="alert-box secondary radius">Ничего не найдено.</li>'
						}
						$("[data-content='okeis-search-result']").html(html_data);

					} else {
						var notification = new NotificationFx({
							wrapper: document.body,
							message: '<p>' + data.message + '</p>',
							layout: 'growl',
							effect: 'genie',
							type: data.status,
							ttl: 3000,
							onClose: function() { return false; },
							onOpen: function() { return false; }
						});
						notification.show();
					}
				}
			}, "json");
		}
	}
});


// Открытие окна просмотра
$("body").delegate("[data-do='open-view-okei']", "click", function(){

	// Получаем информацию
	$.post("/tenders/ajax/get-okei/", {
		okei_id:             $(this).data('id'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {
			if ('success' == data.status){

				// Заполняем значение полей
				$('#view-okei-id').val(data.okei['id']);
				$('#view-okei-full-name').text(data.okei['full_name']);
				$('#view-okei-section').text(data.okei['section']);
				$('#view-okei-group').text(data.okei['group']);
				$('#view-okei-local-name').text(data.okei['local_name']);
				$('#view-okei-international-name').text(data.okei['international_name']);
				$('#view-okei-local-symbol').text(data.okei['local_symbol']);
				$('#view-okei-international-symbol').text(data.okei['international_symbol']);

				// Открываем окно
				$('#modal-view-okei').foundation('reveal', 'open');

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
