$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

function push() {
	var formData = $('input:not([type="checkbox"])').serializeObject();
	$('input[type="checkbox"]').each(function() {
		formData[$(this).attr('name')] = $(this).prop('checked');
	});
	$.post('/set', formData);
}

$(function() {
	$('form').change(function() {
		push();
		$.get('/ui', function(response) {
			$('#ui-response').text(JSON.stringify(response));
		});
		$.get('/game', function(response) {
			$('#game-response').text(JSON.stringify(response));
		});
	});
	$('form').trigger('change');
});