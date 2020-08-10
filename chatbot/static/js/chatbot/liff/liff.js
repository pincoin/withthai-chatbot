window.onload = function (e) {
    const liffId = '1654038916-kOX5RXl4'
    // https://developers.line.biz/en/reference/liff/#initialize-liff-app
    liff.init({
        liffId: liffId
    }).then(() => {
        getProfile();
        initializeApp();
    }).catch((err) => {
        console.log('error')
    });

    // LIFF アプリを閉じる
    // https://developers.line.me/ja/reference/liff/#liffclosewindow()
    document.getElementById('closewindowbutton').addEventListener('click', function () {
        liff.closeWindow();
    });

    // ウィンドウを開く
    // https://developers.line.me/ja/reference/liff/#liffopenwindow()
    document.getElementById('openwindowbutton').addEventListener('click', function () {
        liff.openWindow({
            url: 'https://line.me'
        });
    });

    document.getElementById('openwindowexternalbutton').addEventListener('click', function () {
        liff.openWindow({
            url: 'https://line.me',
            external: true
        });
    });

    // メッセージの送信
    document.getElementById('sendmessagebutton').addEventListener('click', function () {
        // https://developers.line.me/ja/reference/liff/#liffsendmessages()
        liff.sendMessages([{
            'type': 'text',
            'text': "You've successfully sent a message! Hooray!"
        }]).then(function () {
            window.alert('Message sent');
        }).catch(function (error) {
            window.alert('Error sending message: ' + error);
        });
    });
};

// プロファイルの取得と表示
function getProfile() {
    // https://developers.line.me/ja/reference/liff/#liffgetprofile()
    liff.getProfile().then(function (profile) {
        document.getElementById('userIdProfileField').textContent = profile.userId;
        document.getElementById('displayNameField').textContent = profile.displayName;
        document.getElementById('statusMessageField').textContent = profile.statusMessage;
    }).catch(function (error) {
        window.alert('Error getting profile: ' + error);
    });
}

function initializeApp(data) {
    document.getElementById('browserLanguage').textContent = liff.getLanguage();
    document.getElementById('sdkVersion').textContent = liff.getVersion();
    document.getElementById('lineVersion').textContent = liff.getLineVersion();
    document.getElementById('isInClient').textContent = liff.isInClient();
    document.getElementById('isLoggedIn').textContent = liff.isLoggedIn();
    document.getElementById('deviceOS').textContent = liff.getOS();
}