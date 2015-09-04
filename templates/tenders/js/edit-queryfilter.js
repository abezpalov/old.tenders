{% if perms.catalog.add_queryfilter or perms.tenders.change_queryfilter %}

// Инициализация
var queryfilter = {
	regions   : [],
	customers : [],
	owners    : [],
	okveds    : [],
	okpds     : [],
	words     : [],
	regions_rebold: function(){
		$("[data-region]").removeClass('bold');
		for (k = 0; k < queryfilter.regions.length; k++) {
			$("[data-region='" + queryfilter.regions[k]['id'] + "']").addClass('bold');
		}
	},
	customers_rebold: function(){
		$("[data-customer]").removeClass('bold');
		for (k = 0; k < queryfilter.customers.length; k++) {
			$("[data-customer='" + queryfilter.customer[k]['id'] + "']").addClass('bold');
		}
	},
	owners_rebold: function(){
		$("[data-owner]").removeClass('bold');
		for (k = 0; k < queryfilter.owners.length; k++) {
			$("[data-owner='" + queryfilter.owner[k]['id'] + "']").addClass('bold');
		}
	},
	okveds_rebold: function(){
		$("[data-okved]").removeClass('bold');
		for (k = 0; k < queryfilter.okveds.length; k++) {
			$("[data-okved='" + queryfilter.okveds[k]['id'] + "']").addClass('bold');
		}
	},
	okpds_rebold: function(){
		$("[data-okpd]").removeClass('bold');
		for (k = 0; k < queryfilter.okpds.length; k++) {
			$("[data-okpd='" + queryfilter.okpds[k]['id'] + "']").addClass('bold');
		}
	},
	words_rebold: function(){
		$("[data-word]").removeClass('bold');
		for (k = 0; k < queryfilter.words.length; k++) {
			$("[data-word='" + queryfilter.words[k]['id'] + "']").addClass('bold');
		}
	},
	rebold: function(){
		this.regions_rebold()
		this.customers_rebold()
		this.owners_rebold()
		this.okveds_rebold()
		this.okpds_rebold()
		this.words_rebold()
	},
	clear: function() {
		$('#modal-edit-queryfilter-header').text('');
		$('#edit-queryfilter-id').val('0');
		$('#edit-queryfilter-name').val('');
		this.regions   = [];
		this.customers = [];
		this.owners    = [];
		this.okveds    = [];
		this.okpds     = [];
		this.words     = [];
		$('#edit-queryfilter-regions-in').prop('checked', true);
		$('#edit-queryfilter-customers-in').prop('checked', true);
		$('#edit-queryfilter-owners-in').prop('checked', true);
		$('#edit-queryfilter-okveds-in').prop('checked', true);
		$('#edit-queryfilter-okpds-in').prop('checked', true);
		$('#edit-queryfilter-words-in').prop('checked', true);
		$('#edit-queryfilter-state').prop('checked', true);
		$('#edit-queryfilter-public').prop('checked', false);
	},
	get_ids: function(os) {
		ids = '';
		for (i = 0; i < os.length; i++) {
			if (i > 0) { ids = ids + ','; }
			ids = ids + os[i].id;
		}
		return ids;
	}
};

{% endif %}

{% if perms.catalog.add_queryfilter %}

// Открытие окна создания
$("body").delegate("[data-do='open-new-queryfilter']", "click", function(){

	// Обнуляем значения
	queryfilter.clear()

	// Красим
	queryfilter.rebold()

	// Открываем модальное окно
	$('#modal-edit-queryfilter').foundation('reveal', 'open');
	return false;
});

{% endif %}

{% if perms.tenders.change_queryfilter %}

// Открытие окна редактирования
$("body").delegate("[data-do='open-edit-queryfilter']", "click", function(){

	// Получаем информацию о загрузчике
	$.post("/tenders/ajax/get-queryfilter/", {
		queryfilter_id: $(this).data('id'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {
			if ('success' == data.status){

				// Заполняем значение полей
				$('#modal-edit-queryfilter-header').text('Редактировать фильтр запроса');
				$('#edit-queryfilter-id').val(data.queryfilter['id']);
				$('#edit-queryfilter-name').val(data.queryfilter['name']);

				queryfilter.regions   = data.queryfilter['regions'];
				queryfilter.customers = data.queryfilter['customers'];
				queryfilter.owners    = data.queryfilter['owners'];
				queryfilter.okveds    = data.queryfilter['okveds'];
				queryfilter.okpds     = data.queryfilter['okpds'];
				queryfilter.words     = data.queryfilter['words'];

				$('#edit-queryfilter-regions-in').prop('checked', data.queryfilter['regions_in']);
				$('#edit-queryfilter-customers-in').prop('checked', data.queryfilter['customers_in']);
				$('#edit-queryfilter-owners-in').prop('checked', data.queryfilter['owners_in']);
				$('#edit-queryfilter-okveds-in').prop('checked', data.queryfilter['okveds_in']);
				$('#edit-queryfilter-okpds-in').prop('checked', data.queryfilter['okpds_in']);
				$('#edit-queryfilter-words-in').prop('checked', data.queryfilter['words_in']);

				$('#edit-queryfilter-state').prop('checked', data.queryfilter['state']);
				$('#edit-queryfilter-public').prop('checked', data.queryfilter['public']);

				// Красим
				queryfilter.rebold()

				// Открываем окно
				$('#modal-edit-queryfilter').foundation('reveal', 'open');

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


{% endif %}

{% if perms.catalog.add_queryfilter or perms.tenders.change_queryfilter %}


// Сохранение
$("body").delegate("[data-do='edit-queryfilter-save']", "click", function(){

	regions_ids   = queryfilter.get_ids(queryfilter.regions)
	customers_ids = queryfilter.get_ids(queryfilter.customers)
	owners_ids    = queryfilter.get_ids(queryfilter.owners)
	okveds_ids    = queryfilter.get_ids(queryfilter.okveds)
	okpds_ids     = queryfilter.get_ids(queryfilter.okpds)
	words_ids     = queryfilter.get_ids(queryfilter.words)

	// Отправляем запрос
	$.post("/tenders/ajax/save-queryfilter/", {
		queryfilter_id            : $('#edit-queryfilter-id').val(),
		queryfilter_name          : $('#edit-queryfilter-name').val(),

		queryfilter_regions_ids   : regions_ids,
		queryfilter_customers_ids : customers_ids,
		queryfilter_owners_ids    : owners_ids,
		queryfilter_okveds_ids    : okveds_ids,
		queryfilter_okpds_ids     : okpds_ids,
		queryfilter_words_ids     : words_ids,

		queryfilter_regions_in    : $('#edit-queryfilter-regions-in').prop('checked'),
		queryfilter_customers_in  : $('#edit-queryfilter-customers-in').prop('checked'),
		queryfilter_owners_in     : $('#edit-queryfilter-owners-in').prop('checked'),
		queryfilter_okveds_in     : $('#edit-queryfilter-okveds-in').prop('checked'),
		queryfilter_okpds_in      : $('#edit-queryfilter-okpds-in').prop('checked'),
		queryfilter_words_in      : $('#edit-queryfilter-words-in').prop('checked'),

		queryfilter_state         : $('#edit-queryfilter-state').prop('checked'),
		queryfilter_public        : $('#edit-queryfilter-public').prop('checked'),
		csrfmiddlewaretoken       : '{{ csrf_token }}'
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
				$("[data-queryfilter-name='" + $('#edit-queryfilter-id').val() + "']").text($('#edit-queryfilter-name').val());
				$("[data-queryfilter-state='" + $('#edit-queryfilter-id').val() + "']").prop('checked', $('#edit-queryfilter-state').prop('checked'));
				$("[data-queryfilter-public='" + $('#edit-queryfilter-id').val() + "']").prop('checked', $('#edit-queryfilter-public').prop('checked'));

				if ('0' == $('#edit-queryfilter-id').val()) {

					// Закрываем окно
					$('#modal-edit-queryfilter').foundation('reveal', 'close');

					// Обновляем страницу
					setTimeout(function () {location.reload();}, 3000);

				} else {

					// Закрываем окно
					$('#modal-edit-queryfilter').foundation('reveal', 'close');

					// Заполняем значение полей
					$('#edit-queryfilter-id').val('0');
					$('#edit-queryfilter-name').val('');
					$('#edit-queryfilter-state').prop('checked', true);
					$('#edit-queryfilter-public').prop('checked', false);

					queryfilter.rebold()

				}
			}
		}
	}, "json");

	return false;
});


// Отмена редактирования
$("body").delegate("[data-do*='edit-queryfilter-cancel']", "click", function(){

	// Обнуляем значения
	queryfilter.clear()

	// Красим
	queryfilter.rebold()

	// Закрываем окно
	$('#modal-edit-queryfilter').foundation('reveal', 'close');

	return false;
});

{% endif %}

{% if perms.tenders.change_queryfilter %}


// Смена статуса
$("body").delegate("[data-do='switch-queryfilter-state']", "click", function(){

	// Отправляем запрос
	$.post("/tenders/ajax/switch-queryfilter-state/", {
		queryfilter_id:      $(this).data('id'),
		queryfilter_state:   $(this).prop('checked'),
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
		}
	}, "json");

	return true;
});


// Смена статуса "публичности"
$("body").delegate("[data-do='switch-queryfilter-public']", "click", function(){

	// Отправляем запрос
	$.post("/tenders/ajax/switch-queryfilter-public/", {
		queryfilter_id:      $(this).data('id'),
		queryfilter_public:  $(this).prop('checked'),
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
		}
	}, "json");

	return true;
});


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
						li = li + '<a data-do="select-okpd" data-id="' + data.okpds[i]['id'] + '" data-okpd="' + data.okpds[i]['id'] + '"><span>' + data.okpds[i]['code'] + '</span><span>' + data.okpds[i]['name'] + '</span></a>'
						if (data.okpds[i].childs_count > 0) {
							li = li + '<ul id="okpd-' + data.okpds[i]['id'] + '-childs"></ul>'
						}
						li = li + '</li>'
						html_data = html_data + li;
					}
					$('#okpd-' + okpd_id + '-childs').html(html_data);
					queryfilter.okpds_rebold()

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


// Поиск по справочнику ОКПД
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
								li = '<li><a data-do="select-okpd" data-id="' + data.okpds[i]['id'] + '" data-okpd="' + data.okpds[i]['id'] + '"><span>' + data.okpds[i]['code'] + '</span><span>' + data.okpds[i]['name'] + '</span></a></li>'
								html_data = html_data + li;
							}
						} else {
							html_data = '<li class="alert-box secondary radius">Ничего не найдено.</li>'
						}
						$("[data-content='okpds-search-result']").html(html_data);
						queryfilter.okpds_rebold()
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


// Выделение элемента Регион
$("body").delegate("[data-do='select-region']", "click", function(){

	region_id = $(this).data('id');

	// Выясняем выбран ли элемент?
	select = true
	for(i = 0; i < queryfilter.regions.length; i++) {
		if (queryfilter.regions[i]['id'] == region_id) {
			select = false;
			break;
		}
	}

	// Получаем объект с сервера
	$.post("/tenders/ajax/get-region/", {
		region_id:           region_id,
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {

			if ('success' == data.status){

				// Меняем состав выбранных элементов
				if (select) {
					add = true;
					for (k = 0; k < queryfilter.regions.length; k++) {
						if (data.region['id'] == queryfilter.regions[k]['id']) {
							add = false;
							break;
						}
					}
					if (add) {
						queryfilter.regions.push(data.region);
					}
				} else {
					old_regions = queryfilter.regions;
					queryfilter.regions = [];

					for (i = 0; i < old_regions.length; i++) {
						if (old_regions[i]['id'] != data.region['id']) {
							queryfilter.regions.push(old_regions[i]);
						}
					}
				}
				queryfilter.regions_rebold()

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
	return false;
});


// Выделение элемента ОКПД
$("body").delegate("[data-do='select-okpd']", "click", function(){

	okpd_id = $(this).data('id');

	// Выясняем выбран ли элемент?
	select = true
	for(i = 0; i < queryfilter.okpds.length; i++) {
		if (queryfilter.okpds[i]['id'] == okpd_id) {
			select = false;
			break;
		}
	}

	// Получаем дочерние объекты с сервера
	$.post("/tenders/ajax/get-okpd-thread/", {
		okpd_id:            okpd_id,
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {

			if ('success' == data.status){

				// Меняем состав выбранных элементов
				if (select) {
					for (i = 0; i < data.okpds.length; i++) {
						add = true;
						for (k = 0; k < queryfilter.okpds.length; k++) {
							if (data.okpds[i]['id'] == queryfilter.okpds[k]['id']) {
								add = false;
								break;
							}
						}
						if (add) {
							queryfilter.okpds.push(data.okpds[i]);
						}
					}
				} else {
					old_okpds = queryfilter.okpds;
					queryfilter.okpds = [];


					for (i = 0; i < old_okpds.length; i++) {
						add = true;
						for (k = 0; k < data.okpds.length; k++) {
							if (old_okpds[i]['id'] == data.okpds[k]['id']) {
								add = false;
								break;
							}
						}
						if (add) {
							queryfilter.okpds.push(old_okpds[i]);
						}
					}
				}
				queryfilter.okpds_rebold()

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
	return false;
});


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

					html_data = "";

					for(i = 0; i < data.okveds.length; i++) {
						selected = false
						for(k = 0; k < queryfilter.okveds.length; k++) {
							if (queryfilter.okveds[k]['id'] == data.okveds[i]['id']) {
								selected = true;
								break;
							}
						}
						li = "<li>";
						if (data.okveds[i].childs_count > 0) {
							li = li + '<i data-do="switch-li-okved-status" data-id="' + data.okveds[i]['id'] + '" data-state="closed" class="fa fa-plus-square-o"></i>';
						} else {
							li = li + '<i class="fa fa-circle-thin"></i>';
						}
						li = li + '<a data-do="select-okved" data-id="' + data.okveds[i]['id'] + '" data-okved="' + data.okveds[i]['id'] + '">';
						if (data.okveds[i]['code']) {
							li = li + '<span>' + data.okveds[i]['code'] + '</span>';
						}
						li = li + '<span>' + data.okveds[i]['name'] + '</span></a>';
						if (data.okveds[i].childs_count > 0) {
							li = li + '<ul id="okved-' + data.okveds[i]['id'] + '-childs"></ul>';
						}
						li = li + '</li>';
						html_data = html_data + li;
					}

					$('#okved-' + okved_id + '-childs').html(html_data);
					queryfilter.okveds_rebold()

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


// Поиск по справочнику ОКВЭД
$("body").delegate("[data-do='okveds-search']", "keypress", function(e){
	var search_text = $(this).val().toLowerCase();
	var key         = e.which;

	if(key == 13) {

		// Если в строке поиска пусто, показываем полный каталог
		if (search_text == '') {
			$("[data-content='okveds-search-result']").addClass('hidden');
			$("[data-content='okveds-catalog']").removeClass('hidden');
			$("[data-content='okveds-search-result']").html('');
		// Иначе, прячем каталог и показываем результаты поиска
		} else {
			$("[data-content='okveds-search-result']").removeClass('hidden');
			$("[data-content='okveds-catalog']").addClass('hidden');

			// Получаем объекты с сервера
			$.post("/tenders/ajax/search-okveds/", {
				search_text:         search_text,
				csrfmiddlewaretoken: '{{ csrf_token }}'
			},
			function(data) {
				if (null != data.status) {

					if ('success' == data.status){

						html_data = "";

						if (data.okveds.length > 0) {
							for(i = 0; i < data.okveds.length; i++) {
								selected = false;
								for(k = 0; k < queryfilter.okveds.length; k++) {
									if (queryfilter.okveds[k]['id'] == data.okveds[i]['id']) {
										selected = true;
										break;
									}
								}
								li = '<li><a data-do="select-okved" data-id="' + data.okveds[i]['id'] + '" data-okved="' + data.okveds[i]['id'] + '"><span>' + data.okveds[i]['code'] + '</span><span>' + data.okveds[i]['name'] + '</span></a></li>'
								html_data = html_data + li;
							}
						} else {
							html_data = '<li class="alert-box secondary radius">Ничего не найдено.</li>'
						}
						$("[data-content='okveds-search-result']").html(html_data);
						queryfilter.okveds_rebold()

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


// Выделение элемента ОКВЭД
$("body").delegate("[data-do='select-okved']", "click", function(){

	okved_id = $(this).data('id');

	// Выясняем выбран ли элемент?
	select = true
	for(i = 0; i < queryfilter.okveds.length; i++) {
		if (queryfilter.okveds[i]['id'] == okved_id) {
			select = false;
			break;
		}
	}

	// Получаем дочерние объекты с сервера
	$.post("/tenders/ajax/get-okved-thread/", {
		okved_id:            okved_id,
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {

			if ('success' == data.status){

				// Меняем состав выбранных элементов
				if (select) {
					for (i = 0; i < data.okveds.length; i++) {
						add = true;
						for (k = 0; k < queryfilter.okveds.length; k++) {
							if (data.okveds[i]['id'] == queryfilter.okveds[k]['id']) {
								add = false;
								break;
							}
						}
						if (add) {
							queryfilter.okveds.push(data.okveds[i]);
						}
					}
				} else {
					old_okveds = queryfilter.okveds;
					queryfilter.okveds = [];

					for (i = 0; i < old_okveds.length; i++) {
						add = true;
						for (k = 0; k < data.okveds.length; k++) {
							if (old_okveds[i]['id'] == data.okveds[k]['id']) {
								add = false;
								break;
							}
						}
						if (add) {
							queryfilter.okveds.push(old_okveds[i]);
						}
					}
				}
				queryfilter.okveds_rebold();

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
	return false;
});

{% endif %}
