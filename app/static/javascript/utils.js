// var utils = {
// 	myFunction: function(p1, p2) {
// 	    return p1 * p2;              // the function returns the product of p1 and p2
// 	}

// 	// print_orderbook: function(book){
// 	// 	var b = '<tr><th>Sell volume</th><th>Price</th><th>Buy volume</th></tr>';
// 	// 	$.each(jQuery.parseJSON(book['sell_side']), function(index, tuple){
// 	// 	b += '<tr><td>' + tuple[1] + '</td><td>' + tuple[0] + '</td><td></td></tr>';
// 	// 	});
// 	// 	$.each(jQuery.parseJSON(book['buy_side']), function(index, tuple){
// 	// 	b += '<tr><td></td><td>' + tuple[0] + '</td><td>' + tuple[1] +'</td></tr>';
// 	// 	});
// 	// 	$('#orderbook_table').html(b);
// 	// }
// };

function get_orderbook_html(book){
    	var b = '<tr><th>Sell volume</th><th>Price</th><th>Buy volume</th></tr>';
      $.each(jQuery.parseJSON(book['sell_side']), function(index, tuple){
        b += '<tr><td class="success">' + tuple[1] + '</td><td class="success"	>' + tuple[0] + '</td><td></td></tr>';
      });
      $.each(jQuery.parseJSON(book['buy_side']), function(index, tuple){
        b += '<tr><td></td><td class="info">' + tuple[0] + '</td><td class="info">' + tuple[1] +'</td></tr>';
      });
      
      return b;
    };