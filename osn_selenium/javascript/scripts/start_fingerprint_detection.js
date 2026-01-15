(function (settings) {
    const CONFIG = {
        BINDING: '__osn_fingerprint_report__',
        SILENT_ERRORS: true,
        EVENTS_OPTIMIZATION: settings.optimize_events
    };

    const hookedRegistry = new WeakSet();
    const sentEvents = new Set();

    function guard(fn, fallback = undefined) {
        try {
            return fn();
        } catch (e) {
            if (!CONFIG.SILENT_ERRORS) console.error('FingerprintHook Error:', e);
            return fallback;
        }
    }

    const Reporter = {
        send(api, method) {
            guard(
                () => {
                    if (CONFIG.EVENTS_OPTIMIZATION) {
                        const key = `${api}:${method}`;
                        if (sentEvents.has(key)) return;
                        sentEvents.add(key);
                    }

                    const reportFn = window[CONFIG.BINDING];

                    if (reportFn && typeof reportFn === 'function') {
                        const payload = JSON.stringify({
                            api: api,
                            method: String(method),
                            stacktrace: (new Error()).stack
                        });

                        reportFn(payload);
                    }
                }
            );
        }
    };

    const Engine = {
        hookMethod(target, methodName, apiName, settings = {}) {
            guard(
                () => {
                    if (!target) return;
                    const proto = target.prototype || target;
                    let original;

                    try { original = proto[methodName]; } catch(e) { return; }

                    if (!original || typeof original !== 'function' || hookedRegistry.has(original)) return;

                    const wrapper = function (...args) {
                        Reporter.send(apiName, methodName);

                        if (settings.wrapArgIndex !== undefined && typeof args[settings.wrapArgIndex] === 'function') {
                            const origCb = args[settings.wrapArgIndex];

                            args[settings.wrapArgIndex] = function(...cbArgs) {
                                Reporter.send(apiName, `${methodName}_cb`);
                                return origCb.apply(this, cbArgs);
                            };
                        }

                        const result = original.apply(this, args);

                        if (settings.onReturn) {
                            guard(() => settings.onReturn(result, Engine));
                        }

                        return result;
                    };

                    hookedRegistry.add(wrapper);
                    hookedRegistry.add(original);

                    try { Object.defineProperty(wrapper, 'name', { value: methodName }); } catch (e) {}
                    try { Object.defineProperty(wrapper, 'toString', { value: () => original.toString() }); } catch (e) {}

                    proto[methodName] = wrapper;
                }
            );
        },

        hookGetter(target, propName, apiName) {
            guard(
                () => {
                    if (!target) return;
                    const proto = target.prototype || target;

                    let desc, current = proto;
                    while (current && !desc) {
                        desc = Object.getOwnPropertyDescriptor(current, propName);
                        current = Object.getPrototypeOf(current);
                    }

                    if (!desc || !desc.get || hookedRegistry.has(desc.get)) return;

                    const originalGet = desc.get;
                    const wrapperGet = function () {
                        Reporter.send(apiName, propName);
                        return originalGet.call(this);
                    };

                    hookedRegistry.add(wrapperGet);
                    hookedRegistry.add(originalGet);

                    Object.defineProperty(proto, propName, { ...desc, get: wrapperGet });
                }
            );
        },

        hookConstructor(className, apiName, settings = {}) {
            guard(
                () => {
                    const OriginalClass = window[className];
                    if (!OriginalClass || hookedRegistry.has(OriginalClass)) return;

                    const Handler = {
                        construct(target, args) {
                            Reporter.send(apiName, 'constructor');

                            if (settings.wrapArgIndex !== undefined && typeof args[settings.wrapArgIndex] === 'function') {
                                const origCb = args[settings.wrapArgIndex];

                                args[settings.wrapArgIndex] = function(...cbArgs) {
                                    Reporter.send(apiName, 'callback');
                                    return origCb.apply(this, cbArgs);
                                };
                            }

                            return new target(...args);
                        }
                    };

                    try {
                        const Wrapped = new Proxy(OriginalClass, Handler);
                        window[className] = Wrapped;
                        hookedRegistry.add(Wrapped);
                    } catch (e) {}
                }
            );
        }
    };

    const TARGETS = {
        canvas: {
            api: 'canvas',
            methods: [
                { target: HTMLCanvasElement, names: ['toDataURL', 'toBlob', 'getContext'] },
                { target: window.CanvasRenderingContext2D, names: ['getImageData', 'measureText', 'isPointInPath', 'fillText', 'strokeText'] },
                { target: window.WebGLRenderingContext, names: ['getParameter', 'getExtension', 'readPixels', 'compileShader', 'linkProgram'], api: 'webgl' },
                { target: window.WebGL2RenderingContext, names: ['getParameter', 'getExtension', 'readPixels', 'compileShader', 'linkProgram'], api: 'webgl' },
                { target: window.navigator.gpu, names: ['requestAdapter'], api: 'webgpu' }
            ]
        },
        audio: {
            api: 'audioContext',
            targets: [window.AudioContext, window.webkitAudioContext, window.OfflineAudioContext, window.BaseAudioContext],
            methods: [
                'createOscillator', 'createAnalyser', 'createDynamicsCompressor',
                'createScriptProcessor', 'createMediaElementSource', 'createMediaStreamSource',
                'decodeAudioData', 'startRendering'
            ],
            props: ['sampleRate', 'baseLatency', 'outputLatency']
        },
        navigator: {
            api: 'navigator',
            target: Navigator,
            props: [
                'userAgent', 'appName', 'appVersion', 'appCodeName', 'language', 'languages',
                'platform', 'cookieEnabled', 'product', 'productSub', 'vendor', 'vendorSub',
                'hardwareConcurrency', 'deviceMemory', 'maxTouchPoints', 'webdriver', 'doNotTrack', 'oscpu',
                'plugins', 'mimeTypes'
            ],
            methods: [
                { name: 'getBattery', api: 'battery' },
                { name: 'getGamepads', api: 'gamepad' },
                { name: 'registerProtocolHandler' },
                { name: 'requestMediaKeySystemAccess', api: 'drm' }
            ]
        },
        screen: {
            api: 'screen',
            target: Screen,
            props: [
                'width', 'height', 'availWidth', 'availHeight', 'colorDepth', 'pixelDepth',
                'orientation', 'availTop', 'availLeft'
            ]
        },
        window: {
            api: 'window',
            target: Window,
            methods: [
                { target: window, name: 'getComputedStyle', api: 'css' },
                { target: window, name: 'fetch', api: 'network' },
                {
                    target: window,
                    name: 'matchMedia',
                    api: 'mediaQuery',
                    settings: {
                        onReturn: (mql, eng) => eng.hookMethod(mql, 'addEventListener', 'mediaQuery')
                    }
                }
            ],
            props: [
                { target: window, name: 'devicePixelRatio', api: 'screen' },
                { target: window, name: 'innerWidth', api: 'layout' },
                { target: window, name: 'innerHeight', api: 'layout' }
            ]
        },
        network: {
            api: 'network',
            methods: [
                { target: window.XMLHttpRequest, name: 'open' },
                { target: window.XMLHttpRequest, name: 'send' },
                { target: window.RTCPeerConnection, names: ['createOffer', 'createAnswer', 'setLocalDescription', 'setRemoteDescription', 'createDataChannel'], api: 'webrtc' }
            ]
        },
        hardware: {
            methods: [
                { target: window.navigator.bluetooth, name: 'requestDevice', api: 'bluetooth' },
                { target: window.navigator.usb, name: 'requestDevice', api: 'usb' },
                { target: window.navigator.clipboard, name: 'readText', api: 'clipboard' },
                { target: window.navigator.clipboard, name: 'writeText', api: 'clipboard' },
                { target: window.navigator.geolocation, name: 'getCurrentPosition', api: 'geolocation', wrapCallbackArg: 0 },
                { target: window.navigator.geolocation, name: 'watchPosition', api: 'geolocation', wrapCallbackArg: 0 },
                { target: window.navigator.permissions, name: 'query', api: 'permissions' }
            ]
        },
        timing: {
            api: 'time',
            methods: [
                { target: Date, names: ['now', 'getTime'] },
                { target: Performance, names: ['now', 'getEntriesByType'], api: 'performance' }
            ]
        },
        dom: {
            api: 'layout',
            methods: [
                { target: HTMLElement, names: ['getBoundingClientRect', 'getClientRects'] },
                { target: Element, names: ['getBoundingClientRect', 'getClientRects'] }
            ],
            props: [
                { target: HTMLElement, names: ['offsetWidth', 'offsetHeight', 'clientWidth', 'clientHeight', 'scrollWidth', 'scrollHeight'] }
            ]
        },
        fonts: {
            api: 'fonts',
            methods: [
                { target: document.fonts, names: ['load', 'check'] }
            ]
        },
        storage: {
            api: 'storage',
            methods: [
                { target: window.indexedDB, name: 'open', api: 'indexedDB' },
                { target: window.localStorage, names: ['getItem', 'setItem'], api: 'localStorage' },
                { target: window.sessionStorage, names: ['getItem', 'setItem'], api: 'sessionStorage' }
            ]
        },
        intl: {
            api: 'intl',
            methods: [
                { target: Intl.Collator, name: 'supportedLocalesOf' },
                { target: Intl.NumberFormat, name: 'supportedLocalesOf' },
                { target: Intl.DateTimeFormat, name: 'supportedLocalesOf' },
                { target: Intl.Collator.prototype, name: 'resolvedOptions' },
                { target: Intl.NumberFormat.prototype, name: 'resolvedOptions' },
                { target: Intl.DateTimeFormat.prototype, name: 'resolvedOptions' }
            ]
        },
        wasm: {
            api: 'wasm',
            methods: [
                { target: WebAssembly, names: ['instantiate', 'compile'] }
            ]
        },
        svg: {
            api: 'svg',
            methods: [
                { target: SVGGraphicsElement, name: 'getBBox' },
                { target: SVGTextContentElement, name: 'getComputedTextLength' }
            ]
        },
        observers: {
            api: 'observer',
            constructors: [
                { name: 'ResizeObserver', settings: { wrapArgIndex: 0 } },
                { name: 'IntersectionObserver', settings: { wrapArgIndex: 0 } },
                { name: 'PerformanceObserver', settings: { wrapArgIndex: 0 } }
            ]
        },
        math: {
            api: 'math',
            methods: [
                { target: Math, names: ['sin', 'cos', 'tan', 'acos', 'asin', 'atan', 'pow', 'sqrt', 'random'] }
            ]
        }
    };

    function init() {
        Object.values(TARGETS).forEach(
            group => {
                if (group.methods) {
                    group.methods.forEach(
                        def => {
                            const isStr = typeof def === 'string';
                            const targetArr = (group.targets || (isStr ? [] : (Array.isArray(def.target) ? def.target : [def.target]))).filter(t => t);

                            targetArr.forEach(
                                t => {
                                    const names = isStr ? [def] : (Array.isArray(def.names) ? def.names : [def.name]);
                                    const api = (isStr ? group.api : def.api) || group.api || 'unknown';
                                    const opts = {};

                                    if (!isStr && def.wrapCallbackArg !== undefined) opts.argIndexToWrap = def.wrapCallbackArg;

                                    if (t) {
                                        names.forEach(name => Engine.hookMethod(t, name, api, opts));
                                    }
                                }
                            );
                        }
                    );
                }

                if (group.props) {
                    group.props.forEach(
                        def => {
                            const isStr = typeof def === 'string';
                            const targetArr = (group.targets || (isStr ? [group.target] : [def.target])).filter(t => t);

                            targetArr.forEach(
                                t => {
                                    const names = isStr ? [def] : (Array.isArray(def.names) ? def.names : [def.name]);
                                    const api = (isStr ? group.api : def.api) || group.api || 'unknown';

                                    if (t) {
                                        names.forEach(name => Engine.hookGetter(t, name, api));
                                    }
                                }
                            );
                        }
                    );
                }

                if (group.constructors) {
                    group.constructors.forEach(
                        def => {
                            const api = group.api || def.api || 'unknown';
                            const settings = def.settings || {};

                            Engine.hookConstructor(def.name, api, settings);
                        }
                    );
                }
            }
        );
    }

    init();
})(__SETTINGS__PLACEHOLDER__);