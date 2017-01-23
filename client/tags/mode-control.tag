<mode-control>
    <div id="mode" name="mode">
        <button name="cool" class="pure-button" onclick={ control }>冷房</button>
        <button name="dry" class="pure-button" onclick={ control }>除湿</button>
        <button name="warm" class="pure-button" onclick={ control }>暖房</button>
        <button name="power_off" class="pure-button power_off" onclick={ control }>オフ</button>
    </div>

    <script>
        var self = this;

        function setActive() {
            let buttons = self.mode.children;

            for(let button of buttons) {
                button.classList.remove('active');
            };

            for(let button of buttons) {
                if(button.name === mode) {
                    button.classList.add('active');
                }
            }
        }

        self.on('mount', () => {
            setActive();
        });

        $.on('stateChanged', () => {
            setActive();
            self.update();
        });

        control(event) {
            let nextMode = event.target.name;
            let nextValue = value;
            let uri = '';
            if(nextMode === 'power_off') {
                uri = endpoint(`/off?username=${username}&token=${token}`);
            } else {
                if(nextValue === 'off') {
                    nextValue = 26;
                }
                uri = endpoint(`/${nextMode}/${nextValue}?username=${username}&token=${token}`);
            }

            getApiJson(uri).then(data => {
                if(data.result) {
        	        mode = data.mode;
                    value = data.value;
                }
                $.trigger('stateChanged');
        	});
        }
    </script>
</mode-control>
