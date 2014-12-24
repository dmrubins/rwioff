var app = app || {};

app.offTogetherView = Backbone.View.extend({
	
  availableTags : {"res_name": ['David', 'Ravi', 'Peter', 'Daniel Oxman', 'Josh Apple'], 'id': ['253', '234','112','1234','34243','1231']},
  ac : null,


  initialize : function(){

    //Create the autocomplete 
    this.ac = $("<input size='50' />");
    this.ac.bind('keydown', function( event ) {
      if ( event .keyCode === $.ui.keyCode.TAB && $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
      }
    });

    var availableTags = this.availableTags;

    this.ac.autocomplete({
      minLength: 0,

      source : function ( request, response ){
      var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );

      temp = Array();
      for (var i = 0; i < availableTags['res_name'].length; i++) {
        if (matcher.test(availableTags['res_name'][i])) {
          temp.push(availableTags['res_name'][i])
        }
      }

      response(temp);
      },
      
      focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = this.value.split(/,\s*/) ;
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
    });
  },


	render : function(){
    this.$el.append(this.ac);
	}


})