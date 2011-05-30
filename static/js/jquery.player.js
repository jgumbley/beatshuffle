/*!
 * jQuery Player v1.0
 * https://github.com/TiuTalk/html5-mp3-player
 */
(function($) {

	$.fn.player = function(method) {

		var methods = {

			init : function(options) {

				this.player.settings = $.extend({}, this.player.defaults, options);

				return this.each(function() {

					var $element = $(this), // reference to the jQuery version of the current DOM element
						element = this;	 // reference to the actual DOM element

					$($.fn.player.settings.playButton).click(function(e) {
						e.preventDefault();
						
						methods.play.apply($element);
					});
					
					$($.fn.player.settings.pauseButton).click(function(e) {
						e.preventDefault();

						methods.pause.apply($element);
					});
					
					$($.fn.player.settings.stopButton).click(function(e) {
						e.preventDefault();

						methods.stop.apply($element);
					});
					
					$($.fn.player.settings.previousButton).click(function(e) {
						e.preventDefault();

						methods.previous.apply($element);
					});
					
					$($.fn.player.settings.nextButton).click(function(e) {
						e.preventDefault();

						methods.next.apply($element);
					});
				});

			},

			getSong: function() {
				return $.fn.player.settings.playlist[$.fn.player.settings.current];
			},

			play: function() {
				var music = $.fn.player.settings.playlist[$.fn.player.settings.current];
				
				if (!soundManager.getSoundById('player'))
					helpers.createSound.apply(this, ['player', music.mp3]);
				
				if (!this.data('soundObject').playState)
					soundManager.play('player');
				else
					soundManager.resume('player');
			},
			
			pause: function() {
				soundManager.pause('player');
			},
			
			resume: function() {
				soundManager.resume('player');
			},
			
			stop: function() {
				soundManager.stop('player');
				soundManager.destroySound('player');
			},
			
			next: function() {
				if ($.fn.player.settings.current >= ($.fn.player.settings.playlist.length - 1))
					return false;
				
				$.fn.player.settings.current++;
				
				methods.stop.apply(this);
				methods.play.apply(this);
			},
			
			previous: function() {
				if ($.fn.player.settings.current <= 0)
					return false;
				
				$.fn.player.settings.current--;

				methods.stop.apply(this);
				methods.play.apply(this);
			}
		}

		var helpers = {
				
			/**
			 * Cria o objeto do soundmanager
			 * 
			 * @param string id ID do objeto do soundmanager
			 */
			createSound: function(id, music) {
				soundManager.createSound({
					id: id,
					
					url: music,
					autoPlay: true,
					
					onfinish: $.fn.player.settings.onFinish,
					onload: $.fn.player.settings.onLoad,
					
					onpause: $.fn.player.settings.onPause,
					onplay: $.fn.player.settings.onPlay,
					onresume: $.fn.player.settings.onResume,
					onstop: $.fn.player.settings.onStop,

					onbeforefinish: $.fn.player.settings.onBeforeFinish(),
					onjustbeforefinish:  function() {
						methods.next.apply(this);
						$.fn.player.settings.onJustBeforeFinish.apply(this);
					},
					onbeforefinishcomplete: $.fn.player.settings.onBeforeFinishComplete,
					
					onid3: $.fn.player.settings.onID3,
					
					whileloading: $.fn.player.settings.whileLoading,
					whileplaying: $.fn.player.settings.whilePlaying
				});
				
				$(this).data('soundObject', soundManager.getSoundById('player'));
			}

		}

		if (methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error( 'Method "' +  method + '" does not exist in player plugin!');
		}

	}

	$.fn.player.defaults = {
		playlist: null,
		current: 0,

		playButton: '.button.play',
		pauseButton: '.button.pause',
		stopButton: '.button.stop',
		
		nextButton: '.button.next',
		previousButton: '.button.previous',
		
		onFinish: function() { },
		onLoad: function() { },
		
		onPause: function() { },
		onPlay: function() { },
		onPosition: function() { },
		onResume: function() { },
		onStop: function() { },

		onBeforeFinish: function() { },
		onJustBeforeFinish: function() { },
		onBeforeFinishComplete: function() { },
		
		onID3: function() { },
		
		whileLoading: function() { },
		whilePlaying: function() { }
	}

	$.fn.player.settings = {}

})(jQuery);