var app = app || {};

app.scheduleModel = Backbone.Model.extend({
	
	defaults: {
		schedule : Array(),
		residents : new app.residentsCollection(),
		pgy : "interns",
	}, 

	initialize : function(){
		this.listenTo(dispatcher, 'change:currentDate', this.onDateChange);
	},

	onDateChange : function(date){
		this.set('currentDate', date);
		this.getResidentsOffForDate();
	}, 

	getResidentsOffForDate: function(){
		//console.log('get residents for date called');
		currentDate = this.get('dateModel').get('currentDate');
		date = $.datepicker.formatDate( "yymmdd", currentDate );

		var residents = new app.residentsCollection();
		var sm = this;

		$.ajax('/' + this.get('pgy') + '/off/' + date)
			.done(function(data){
				//console.log(data);
				data = $.parseJSON(data);
				names = data.names;
				blocks = data.blocks;
				//ids = data.ids;
				for (var i = 0; i < names.length; i++){
					residents.add(new app.residentOffForDayModel({'name': names[i], 'block': blocks[i]}) ) ;
				}
				sm.set('residents' , residents);
				console.log(residents.size())
				residents.getEmails();
			})		
	}

})