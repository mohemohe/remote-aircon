<value-control>
    <div id="updown">
        <button name="up" class="pure-button" onclick={ control }>
            <i class="fa fa-chevron-up" aria-hidden="true"></i>
        </button>
        <button name="down" class="pure-button" onclick={ control }>
            <i class="fa fa-chevron-down" aria-hidden="true"></i>
        </button>
    </div>

    <script>
        let lock = false;
        control(event) {
            if(lock) {
                return false;
            }

            lock = true;
            let nextValue = value;
            if(event.target.name === 'up') {
                nextValue++;
            } else {
                nextValue--;
            }
            getApiJson(endpoint(`/${mode}/${nextValue}?username=${username}&token=${token}`)).then(data => {
                if(data.result) {
                mode = data.mode;
                    value = data.value;
                }
                $.trigger('stateChanged');
                lock = false;
            });
        }
    </script>
</value-control>
