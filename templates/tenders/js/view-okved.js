// Открытие/закрытие ветви категорий ОКВЭД
$("body").delegate("[data-do='switch-li-okved-status']", "click", function(){
	if ($(this).data('state') == 'closed') {

		okved_id = $(this).data('id')

		// Получаем дочерние объекты с сервера
		$.post("/tenders/ajax/get-okved-childrens/", {
			okved_id:            $(this).data('id'),
			csrfmiddlewaretoken: '{{ csrf_token }}'
		},
		function(data) {
			if (null != data.status) {

				if ('success' == data.status){

					html_data = ""

					for(i = 0; i < data.okveds.length; i++) {
						li = "<li>"
						if (data.okveds[i].childs_count > 0) {
							li = li + '<i data-do="switch-li-okved-status" data-id="' + data.okveds[i]['id'] + '" data-state="closed" class="fa fa-plus-square-o"></i>'
						} else {
							li = li + '<i class="fa fa-circle-thin"></i>'
						}
						if (data.okveds[i]['code']) {
							li = li + '<span>' + data.okveds[i]['code'] + '</span>'
						}
						li = li + '<span>' + data.okveds[i]['name'] + '</span>'
						if (data.okveds[i].childs_count > 0) {
							li = li + '<ul id="okved-' + data.okveds[i]['id'] + '-childs"></ul>'
						}

						li = li + '</li>'

						html_data = html_data + li;
					}

					$('#okved-' + okved_id + '-childs').html(html_data);

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

