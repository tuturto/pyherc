;; -*- coding: utf-8 -*-
;;
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

(require pyherc.aspects)
(require pyherc.macros)
(import [pyherc.rules.public [ActionParameters]]
	[pyherc.aspects [log-debug log-info]])

(defn morph [character new-character-name action-factory
             &optional [destroyed-characters #t()]]
  "perform morph on a character"
  (let [[action (.get-action action-factory
				(MetamorphosisParameters character 
                                                         new-character-name
                                                         destroyed-characters))]]
    (when (.legal? action)
      (.execute action))))

(defn morph-legal? [character new-character-name action-factory
                    &optional [destroyed-characters #t()]]
  "can morph be performed"
  (let [[action (.get-action action-factory
                             (MetamorphosisParameters character
                                                      new-character-name
                                                      destroyed-characters))]]
    (.legal? action)))

(defclass MetamorphosisParameters [ActionParameters]
  "Class controlling creation of MorphAction"
  [[--init-- #d(fn [self character new-character-name destroyed-characters]
		 (-> (super) (.--init--))
		 (setv self.action-type "metamorphosis")
		 (setv self.character character)
                 (setv self.new-character-name new-character-name)
                 (setv self.destroyed-characters destroyed-characters)
		 nil)]])
