//install service worker
self.addEventListener('install', evt => {
    console.log('service worker has been installed');
});

//activation of service worker
self.addEventListener('install', evt => {
    console.log('service worker has is activated');
});