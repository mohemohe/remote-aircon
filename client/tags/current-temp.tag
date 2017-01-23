<current-temp>
    <div id="temp">{value}</div>

    <script>
        let self = this;
        self.value = ' ';

        $.on('stateChanged', () => {
            self.value = value;
            self.update();
        });
    </script>
</current-temp>
