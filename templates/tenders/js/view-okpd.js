// Открытие/закрытие ветви категорий ОКПД
$("body").delegate("[data-do='switch-li-okpd-status']", "click", function(){
	if ($(this).data('state') == 'closed') {

		okpd_id = $(this).data('id')

		// Получаем дочерние объекты с сервера
		$.post("/tenders/ajax/get-okpd-childrens/", {
			okpd_id:             $(this).data('id'),
			csrfmiddlewaretoken: '{{ csrf_token }}'
		},
		function(data) {
			if (null != data.status) {

				if ('success' == data.status){

					html_data = ""

					for(i = 0; i < data.okpds.length; i++) {
						li = "<li>"
						if (data.okpds[i].childs_count > 0) {
							li = li + '<i data-do="switch-li-okpd-status" data-id="' + data.okpds[i]['id'] + '" data-state="closed" class="fa fa-plus-square-o"></i>'
						} else {
							li = li + '<i class="fa fa-circle-thin"></i>'
						}
						li = li + '<span>' + data.okpds[i]['code'] + '</span>'
						li = li + '<span>' + data.okpds[i]['name'] + '</span>'
						if (data.okpds[i].childs_count > 0) {
							li = li + '<ul id="okpd-' + data.okpds[i]['id'] + '-childs"></ul>'
						}

						li = li + '</li>'

						html_data = html_data + li;
					}

					$('#okpd-' + okpd_id + '-childs').html(html_data);

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

		$(this).parent("li").removeClass('closed');
		$(this).parent("li").addClass('opened');
		$(this).removeClass('fa-plus-square-o');
		$(this).addClass('fa-minus-square-o');
		$(this).data('state', 'opened');

	} else {
		$(this).parent("li").removeClass('opened');
		$(this).parent("li").addClass('closed');
		$(this).removeClass('fa-minus-square-o');
		$(this).addClass('fa-plus-square-o');
		$(this).data('state', 'closed');
	}
	return false;
});


// Поиск по справочнику
$("body").delegate("[data-do='okpds-search']", "keypress", function(e){
	var search_text = $(this).val().toLowerCase();
	var key         = e.which;

	if(key == 13) {

		// Если в строке поиска пусто, показываем полный каталог
		if (search_text == '') {
			$("[data-content='okpds-search-result']").addClass('hidden');
			$("[data-content='okpds-catalog']").removeClass('hidden');
			$("[data-content='okpds-search-result']").html('');
		// Иначе, прячем каталог и показываем результаты поиска
		} else {
			$("[data-content='okpds-search-result']").removeClass('hidden');
			$("[data-content='okpds-catalog']").addClass('hidden');

			// Получаем объекты с сервера
			$.post("/tenders/ajax/search-okpds/", {
				search_text:         search_text,
				csrfmiddlewaretoken: '{{ csrf_token }}'
			},
			function(data) {
				if (null != data.status) {

					if ('success' == data.status){

						html_data = ""

						if (data.okpds.length > 0) {
							for(i = 0; i < data.okpds.length; i++) {
								li = '<li><span>' + data.okpds[i]['code'] + '</span><span>' + data.okpds[i]['name'] + '</span></li>'
								html_data = html_data + li;
							}
						} else {
							html_data = '<li class="alert-box secondary radius">Ничего не найдено.</li>'
						}
						$("[data-content='okpds-search-result']").html(html_data);

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
