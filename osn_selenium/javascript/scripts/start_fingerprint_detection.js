function start_fingerprint_detection(settings) {
    const CONFIG = {
        BINDING: '__osn_fingerprint_report__',
        SILENT_ERRORS: true,
        EVENTS_OPTIMIZATION: settings.optimize_events
    };

    const MODIFIERS = {};
__MODIFIERS_PLACEHOLDER__

    const STORAGE = new Map();

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
        send(api, target, method) {
            guard(() => {
                if (CONFIG.EVENTS_OPTIMIZATION) {
                    const key = `${api}:${target}:${method}`;

                    if (sentEvents.has(key)) return;

                    sentEvents.add(key);
                }

                const reportFn = window[CONFIG.BINDING];

                if (typeof reportFn === 'function') {
                    const stack = (new Error()).stack;

                    const payload = JSON.stringify({
                        api: api,
                        used_method: `${target}.${method}`,
                        stacktrace: stack
                    });

                    reportFn(payload);
                }
            });
        }
    };

__DETECTION_PLACEHOLDER__
}

start_fingerprint_detection(__SETTINGS__PLACEHOLDER__);