"use strict";
(self["webpackChunkjupyterlab_skip_traceback"] = self["webpackChunkjupyterlab_skip_traceback"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_coreutils"],{

/***/ "./lib/SkipTracebackWidget.js":
/*!************************************!*\
  !*** ./lib/SkipTracebackWidget.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_apputils_lib_clipboard__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils/lib/clipboard */ "./node_modules/@jupyterlab/apputils/lib/clipboard.js");




const BTN_BASE_CLASS = 'minimal jp-Button';
const COPY_CLASS = `fa fa-fw fa-copy ${BTN_BASE_CLASS} right-align`;
const TOGGLE_CLOSED_CLASS = `fa fa-caret-right jp-ToolbarButtonComponent ${BTN_BASE_CLASS}`;
const TOGGLE_OPENED_CLASS = `fa fa-caret-down jp-ToolbarButtonComponent ${BTN_BASE_CLASS}`;
const SHORT_ERROR_CLASS = 'short-error';
const RED_BOLD_TEXT_CLASS = 'red-bold-text';
const setMessageInCollapsedState = (shortError, data) => {
    const eName = document.createElement('span');
    eName.className = RED_BOLD_TEXT_CLASS;
    eName.textContent = data.ename;
    const eValue = document.createTextNode(`: ${data.evalue}`);
    shortError.innerHTML = '';
    shortError.appendChild(eName);
    shortError.appendChild(eValue);
};
// prettier-ignore
class SkipTracebackWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor(options) {
        super();
        this._mimeType = options.mimeType;
        this._options = options;
    }
    static setDefaults(newDefaults) {
        SkipTracebackWidget._defaults = {
            ...SkipTracebackWidget._defaults,
            ...newDefaults,
        };
    }
    _toggleTraceback() {
        if (this._toggleBtn && this._tracebackNode && this._shortError && this._data) {
            const isToggled = this._toggleBtn.className === TOGGLE_CLOSED_CLASS;
            if (isToggled) {
                this._toggleBtn.className = TOGGLE_OPENED_CLASS;
                this._shortError.innerHTML = '';
                this.node.appendChild(this._tracebackNode);
            }
            else {
                this._toggleBtn.className = TOGGLE_CLOSED_CLASS;
                setMessageInCollapsedState(this._shortError, this._data);
                this.node.removeChild(this._tracebackNode);
            }
        }
    }
    _copyTraceback() {
        if (this._tracebackNode) {
            _jupyterlab_apputils_lib_clipboard__WEBPACK_IMPORTED_MODULE_3__.Clipboard.copyToSystem(this._tracebackNode.textContent || '');
        }
    }
    renderModel(model) {
        this._data = model.data[this._mimeType];
        const toggleBtn = document.createElement('button');
        toggleBtn.className = TOGGLE_CLOSED_CLASS;
        toggleBtn.onclick = this._toggleTraceback.bind(this);
        this._toggleBtn = toggleBtn;
        const shortError = document.createElement('pre');
        shortError.className = SHORT_ERROR_CLASS;
        setMessageInCollapsedState(shortError, this._data);
        shortError.onclick = this._toggleTraceback.bind(this);
        this._shortError = shortError;
        const copyBtn = document.createElement('button');
        copyBtn.className = COPY_CLASS;
        copyBtn.onclick = this._copyTraceback.bind(this);
        copyBtn.title = 'Copy full traceback to clipboard';
        const span = document.createElement('div');
        span.className = 'skip-traceback';
        span.appendChild(copyBtn);
        span.appendChild(toggleBtn);
        span.appendChild(shortError);
        const traceback = document.createElement('pre');
        // It should look like stderr
        const source = model.data['application/vnd.jupyter.stderr'] ||
            this._data.traceback.join('\n');
        let renderedPromise;
        if (typeof _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.renderError !== 'undefined') {
            renderedPromise = (0,_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.renderError)({
                ...this._options,
                host: traceback,
                source
            });
        }
        else {
            renderedPromise = (0,_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.renderText)({
                ...this._options,
                host: traceback,
                source
            });
        }
        const tbDiv = document.createElement('div');
        tbDiv.className = 'jp-RenderedText';
        tbDiv.setAttribute('data-mime-type', 'application/vnd.jupyter.stderr');
        tbDiv.appendChild(traceback);
        // End hack due to issue
        this._tracebackNode = tbDiv;
        this.node.appendChild(span);
        if (!SkipTracebackWidget._defaults.collapsed) {
            this._toggleTraceback();
        }
        // Don't finish until we render the text
        return renderedPromise;
    }
}
SkipTracebackWidget._defaults = {
    collapsed: true,
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SkipTracebackWidget);


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   rendererFactory: () => (/* binding */ rendererFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _SkipTracebackWidget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./SkipTracebackWidget */ "./lib/SkipTracebackWidget.js");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);



/**
 * The default mime type for the extension.
 */
const MIME_TYPE = 'application/vnd.jupyter.error';
const PLUGIN_NAME = 'jupyterlab-skip-traceback';
/**
 * A mime renderer factory for jupyter_exec_error data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [MIME_TYPE],
    createRenderer: (options) => new _SkipTracebackWidget__WEBPACK_IMPORTED_MODULE_1__["default"](options),
};
/**
 * Extension definition.
 */
const extension = {
    id: 'jupyterlab-skip-traceback:rendermime',
    rendererFactory,
    rank: 0,
    dataType: 'json',
};
const extensionSettings = {
    id: `${PLUGIN_NAME}:plugin`,
    autoStart: true,
    requires: [_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__.IRenderMimeRegistry, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    activate: function (app, rendermime, settingRegistry) {
        function updateSettings(settings) {
            const enabled = settings.get('enabled').composite;
            if (enabled) {
                // Safe to do multiple times as the code replaces the current one
                rendermime.addFactory(extension.rendererFactory, extension.rank);
            }
            else {
                // We assume we were the only mime render ever installed and nothing removed us already
                extension.rendererFactory.mimeTypes.forEach(type => rendermime.removeMimeType(type));
            }
            const collapsed = settings.get('collapsed').composite;
            _SkipTracebackWidget__WEBPACK_IMPORTED_MODULE_1__["default"].setDefaults({ collapsed });
        }
        settingRegistry.load(`${PLUGIN_NAME}:settings`).then((settings) => {
            updateSettings(settings);
            settings.changed.connect(updateSettings);
        }, (err) => {
            console.error(`Could not load settings, so did not active ${PLUGIN_NAME}: ${err}`);
        });
        // eslint-disable-next-line no-console
        console.log('JupyterLab extension jupyterlab-skip-traceback is activated!');
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extensionSettings);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.skip-traceback {
  background-color: var(--jp-rendermime-error-background);
  font-family: var(--jp-code-font-family);
  color: var(--jp-content-font-color1);
}

.skip-traceback > button {
  background-color: transparent;
  padding: 1px;
  margin: 2px;
  display: inline;
  border: 0;
}

.skip-traceback > button:hover {
  background-color: #ffb9b9;
}

.skip-traceback > button:active {
  background-color: #ff9090;
}

.skip-traceback > .short-error {
  display: inline;
}

.skip-traceback > .fa-copy {
  border: dotted;
  border-width: 1px;
  min-height: unset;
  min-width: unset;
}

.skip-traceback > .fa-caret-right,
.skip-traceback > .fa-caret-down {
  /* To fix shifting of text to the right when toggled */
  width: 17px;
  height: 17px;
}

.skip-traceback > .right-align {
  float: right;
}

.skip-traceback .red-bold-text {
  color: #b22b31;
  font-weight: bold;
}
`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;EACE,uDAAuD;EACvD,uCAAuC;EACvC,oCAAoC;AACtC;;AAEA;EACE,6BAA6B;EAC7B,YAAY;EACZ,WAAW;EACX,eAAe;EACf,SAAS;AACX;;AAEA;EACE,yBAAyB;AAC3B;;AAEA;EACE,yBAAyB;AAC3B;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,cAAc;EACd,iBAAiB;EACjB,iBAAiB;EACjB,gBAAgB;AAClB;;AAEA;;EAEE,sDAAsD;EACtD,WAAW;EACX,YAAY;AACd;;AAEA;EACE,YAAY;AACd;;AAEA;EACE,cAAc;EACd,iBAAiB;AACnB","sourcesContent":[".skip-traceback {\n  background-color: var(--jp-rendermime-error-background);\n  font-family: var(--jp-code-font-family);\n  color: var(--jp-content-font-color1);\n}\n\n.skip-traceback > button {\n  background-color: transparent;\n  padding: 1px;\n  margin: 2px;\n  display: inline;\n  border: 0;\n}\n\n.skip-traceback > button:hover {\n  background-color: #ffb9b9;\n}\n\n.skip-traceback > button:active {\n  background-color: #ff9090;\n}\n\n.skip-traceback > .short-error {\n  display: inline;\n}\n\n.skip-traceback > .fa-copy {\n  border: dotted;\n  border-width: 1px;\n  min-height: unset;\n  min-width: unset;\n}\n\n.skip-traceback > .fa-caret-right,\n.skip-traceback > .fa-caret-down {\n  /* To fix shifting of text to the right when toggled */\n  width: 17px;\n  height: 17px;\n}\n\n.skip-traceback > .right-align {\n  float: right;\n}\n\n.skip-traceback .red-bold-text {\n  color: #b22b31;\n  font-weight: bold;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `
`, "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_coreutils.371c87394cdfe635f1e1.js.map