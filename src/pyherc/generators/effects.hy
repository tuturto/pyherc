;; -*- coding: utf-8 -*-

;; Copyright (c) 2010-2015 Tuukka Turto
;; 
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;; 
;; The above copyright notice and this permission notice shall be included in
;; all copies or substantial portions of the Software.
;; 
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
;; THE SOFTWARE.

(import [functools [partial]])
(import [copy [deepcopy]])
(import [pyherc.aspects [log-debug log-info]])
(require pyherc.aspects)
(require hy.contrib.anaphoric)

#i(defn get-effect-creator [effect-config]
    "get a function to create effects"
    (partial create-effect effect-config))

#d(defn create-effect [effect-config key &kwargs kwargs]
    "instantiates new effect with given parameters"
    (let [[config (get effect-config key)]
	  [params (deepcopy config)]
	  [effect-type (.pop params "type")]]
      (if params
	(ap-each kwargs (do
			 (when (in it params) (.pop params it))
			 (assoc params it (get kwargs it))))
	(setv params kwargs))
      (apply effect-type [] params)))
