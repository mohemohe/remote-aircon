<login-form>
    <form id="login" class="pure-form pure-form-stacked" onsubmit={ login }>
        <label>アカウントID: <input name="username" type="text"></label>
        <label>パスワード: <input name="raw_password" type="password"></label>
        <button id="login_button" class="pure-button">ログイン</button>
        <div id="login_info" name="login_info"></div>
    </form>

    <script>
        let self = this;

        login(event) {
            event.preventDefault();

            let self_username = self.username.value;
            let raw_password = self.raw_password.value;

            let sha512 = new jsSHA('SHA-512', 'TEXT');
        	sha512.update(raw_password);
        	let password = sha512.getHash('HEX');

        	let form = new FormData();
        	form.append('username', self_username);
        	form.append('password', password);

            postApiJson(endpoint('/login'), form).then(data => {
                if(data.result) {
                    username = self_username;
                    token = data.token;

                    localStorage.username = username;
                    localStorage.token = token;

                    riot.mount('aircon-control');
                    self.unmount(true);
                } else {
                    self.login_info.innerHTML = data.message;
                }
            });
        }
    </script>
</login-form>
