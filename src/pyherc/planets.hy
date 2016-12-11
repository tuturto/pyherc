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

;; based on code by Paul Schlyter at http://www.stjarnhimlen.se/comp/ppcomp.html

(import math)

(defn sinᵒ [x]
  (math.sin (math.radians x)))

(defn cosᵒ [x]
  (math.cos (math.radians x)))

(defn atan2ᵒ [y x]
  (math.degrees (math.atan2 y x)))

(defn ast-date [d]
  "create date representation"
  (+ (* (. d year) 367)
     (- (// (* 7 (+ (. d year) (// (+ (. d month) 9) 12))) 4))
     (// (* (. d month) 275) 9)
     (. d day)
     -730530
     (/ (if (hasattr d "hour")
          (. d hour)
          1.0)
        24.0)))

(defn normalize-angle [n]
  "normalize angle so that 0 <= n <= 360"
  (when n (- n (* 360 (// n 360)))))

(defn new-orbit [name date long-ascending-node inclination arg-perihelion
                 semi-major-axis eccentricity mean-anomaly]
  "create data structure representing orbital elements"
  {:name name
   :date date
   :long-ascending-node (normalize-angle long-ascending-node)
   :inclination (normalize-angle inclination)
   :arg-perihelion (normalize-angle arg-perihelion)
   :semi-major-axis semi-major-axis
   :eccentricity eccentricity
   :mean-anomaly (normalize-angle mean-anomaly)})

(defn mean-anomaly [orbit]
  (:mean-anomaly orbit))

(defn eccentricity [orbit]
  (:eccentricity orbit))

(defn semi-major-axis [orbit]
  "semi-major axis or mean distance"
  (:semi-major-axis orbit))

(defn longitude-ascending-node [orbit]
  (:long-ascending-node orbit))

(defn inclination [orbit]
  (:inclination orbit))

(defn argument-perihelion [orbit]
  (:arg-perihelion orbit))

(setv zodiacs [(, 00 30 'krios)
               (, 30 60 'tavros)
               (, 60 90 'didimoi)
               (, 90 120 'karkinos)
               (, 120 150 'leon)
               (, 150 180 'parthenos)
               (, 180 210 'zygos)
               (, 210 240 'skorpios)
               (, 240 270 'toksotis)
               (, 270 300 'aigokeros)
               (, 300 330 'ydrohoos)
               (, 330 360 'ihtheis)])

(defn ra-to-zodiac [ra]
  "convert RA to respective zodiac"
  (get (first (filter (fn [x]
                        (<= (first x) (normalize-angle ra) (second x)))
                      zodiacs))
       2))

(setv orbits {})

(defn register-orbit [body func]
  (assoc orbits body func))

(register-orbit 'helios
                (fn [d]
                  "orbital elements of sun/helios on a given date"
                  (new-orbit :name 'helios
                             :date d
                             :long-ascending-node nil
                             :arg-perihelion (+ 282.9404 (* 4.70935E-5 
                                                            (ast-date d)))
                             :semi-major-axis 1.0
                             :eccentricity (- 0.016709 (* 1.151E-9
                                                          (ast-date d)))
                             :mean-anomaly (+ 356.0470 (* 0.9856002585
                                                          (ast-date d)))
                             :inclination 0.0)))

(register-orbit 'selene
                (fn [d]
                  "orbital elements of moon/selene on a given date"
                  (new-orbit :name 'selene
                             :date d
                             :long-ascending-node (- 125.1228 (* 0.0529538083
                                                                 (ast-date d)))
                             :arg-perihelion (+ 318.0634 (* 0.1643573223
                                                            (ast-date d)))
                             :semi-major-axis 60.2666
                             :eccentricity 0.054900
                             :mean-anomaly (+ 115.3654 (* 13.0649929509
                                                          (ast-date d)))
                             :inclination 5.1454)))

(register-orbit 'hermes
                (fn [d]
                  "orbital elements of mercury/hermes on a given date"
                  (new-orbit :name 'hermes
                             :date d
                             :long-ascending-node (+ 48.3313 (* 3.24587E-5
                                                                (ast-date d)))
                             :arg-perihelion (+ 29.1241 (* 1.01444E-5
                                                           (ast-date d)))
                             :semi-major-axis 0.387098
                             :eccentricity (+ 0.205635 (* 5.59E-10
                                                          (ast-date d)))
                             :mean-anomaly (+ 168.6562 (* 4.0923344368
                                                          (ast-date d)))
                             :inclination (+ 7.0047 (* 5.00E-8
                                                       (ast-date d))))))

(register-orbit 'aphrodite
                (fn [d]
                  "orbital element of venus/aphrodite on a given date"
                  (new-orbit :name 'aphrodite
                             :date d
                             :long-ascending-node (+ 76.6799 (* 2.46590E-5
                                                                (ast-date d)))
                             :inclination (+ 3.3946 (* 2.75E-8
                                                       (ast-date d)))
                             :arg-perihelion (+ 54.8910 (* 1.38374E-5
                                                           (ast-date d)))
                             :semi-major-axis 0.723330
                             :eccentricity (- 0.006773 (* 1.302E-9
                                                          (ast-date d)))
                             :mean-anomaly (+ 48.0052 (* 1.6021302244
                                                         (ast-date d))))))

(register-orbit 'ares
                (fn [d]
                  "orbital elements of mars/ares on a given date"
                  (new-orbit :name 'ares
                             :date d
                             :long-ascending-node (+ 49.5574 (* 2.11081E-5
                                                                (ast-date d)))
                             :inclination (- 1.8497 (* 1.78E-8
                                                       (ast-date d)))
                             :arg-perihelion (+ 286.5016 (* 2.92961E-5
                                                            (ast-date d)))
                             :semi-major-axis 1.523688
                             :eccentricity (+ 0.093405 (* 2.516E-9
                                                          (ast-date d)))
                             :mean-anomaly (+ 18.6021 (* 0.5240207766
                                                         (ast-date d))))))

(register-orbit 'dias
                (fn [d]
                  "orbital elements of dias/jupiter on a given date"
                  (new-orbit :name 'dias
                             :date d
                             :long-ascending-node (+ 100.4542 (* 2.76854E-5
                                                                 (ast-date d)))
                             :inclination (- 1.3030 (* 1.557E-7
                                                       (ast-date d)))
                             :arg-perihelion (+ 273.8777 (* 1.64505E-5
                                                            (ast-date d)))
                             :semi-major-axis 5.20256
                             :eccentricity (+ 0.048498 (* 4.469E-9
                                                          (ast-date d)))
                             :mean-anomaly (+ 19.8950 (* 0.0830853001
                                                         (ast-date d))))))

(register-orbit 'cronus
                (fn [d]
                  "orbital elements of saturn/cronus on a given date"
                  (new-orbit :name 'saturn
                             :date d
                             :long-ascending-node (+ 113.6634 (* 2.38980E-5
                                                                 (ast-date d)))
                             :inclination (- 2.4886 (* 1.081E-7
                                                       (ast-date d)))
                             :arg-perihelion (+ 339.3939 (* 2.97661E-5
                                                            (ast-date d)))
                             :semi-major-axis 9.55475
                             :eccentricity (- 0.055546 (* 9.499E-9
                                                          (ast-date d)))
                             :mean-anomaly (+ 316.9670 (* 0.0334442282
                                                          (ast-date d))))))

(defn orbit [body d]
  ((get orbits body) d))

(defn obliquity-of-ecliptic [d]
  "obliquity of the ecliptic"
  (- 23.4393 (* 3.563E-7 (ast-date d))))

(defn mean-longitude [orbit]
  (normalize-angle (+ (argument-perihelion orbit)
                      (mean-anomaly orbit))))

(defn eccentric-anomaly [orbit]
  "calculate eccentric-anomaly for orbit"
  (defn iterate [e0]
    (- e0 (/ (- e0 
                (* (/ 180.0 math.pi) 
                   (eccentricity orbit) 
                   (sinᵒ e0)) 
                (mean-anomaly orbit))
             (- 1 
                (* (eccentricity orbit) 
                   (cosᵒ e0))))))
  (setv e1 (+ (mean-anomaly orbit)
              (* (/ 180.0 math.pi)
                 (eccentricity orbit) (sinᵒ (mean-anomaly orbit))
                 (+ 1 (* (eccentricity orbit)
                         (cosᵒ (mean-anomaly orbit)))))))
  (if (< (eccentricity orbit) 0.03)
    e1
    (do (setv e0 e1)
        (setv e1 (iterate e0))
        (setv limit 20)
        (while (and (> (abs (- e0 e1)) 0.000000005)
                    (> limit 0))
          (setv limit (dec limit))
          (setv e0 e1)
          (setv e1 (iterate e0)))
        e1)))

(defn distance-true-anomaly [orbit]
  "calculate distance and true anomaly for a planet in given orbit"
  (defn ecliptic-coordinates []
  (, (* (semi-major-axis orbit)
        (- (cosᵒ (eccentric-anomaly orbit))
           (eccentricity orbit)))
     (* (semi-major-axis orbit)
        (math.sqrt (- 1 (pow (eccentricity orbit) 2)))
        (sinᵒ (eccentric-anomaly orbit)))))
  
  (let [[(, x y) (ecliptic-coordinates)]]
    (, (math.sqrt (+ (pow x 2)
                     (pow y 2)))
       (atan2ᵒ y x))))

(defn heliocentric-location [dist-true-anomaly orbit]
  "compute heliocentric position"
  (let [[(, distance true-anomaly) dist-true-anomaly]]
    (, (* distance (- (* (cosᵒ (longitude-ascending-node orbit)) 
                         (cosᵒ (+ true-anomaly (argument-perihelion orbit)))) 
                      (* (sinᵒ (longitude-ascending-node orbit)) 
                         (sinᵒ (+ true-anomaly (argument-perihelion orbit))) 
                         (cosᵒ (inclination orbit)))))
       (* distance (+ (* (sinᵒ (longitude-ascending-node orbit)) 
                         (cosᵒ (+ true-anomaly (argument-perihelion orbit)))) 
                      (* (cosᵒ (longitude-ascending-node orbit)) 
                         (sinᵒ (+ true-anomaly (argument-perihelion orbit))) 
                         (cosᵒ (inclination orbit)))))
       (* distance 
          (sinᵒ (+ true-anomaly (argument-perihelion orbit))) 
          (sinᵒ (inclination orbit))))))

(defn lon-lat [h-loc]
  "convert heliocentric location to longitude-latitude pair in ecliptica"
  (let [[(, x y z) h-loc]]
      (, (normalize-angle (atan2ᵒ y x))
         (atan2ᵒ z (math.sqrt (+ (pow x 2) (pow y 2)))))))

(defn sun-long [orbit]
  "longitude of sun"
  (let [[(, distance true-anomaly) (distance-true-anomaly orbit)]]
    (normalize-angle (+ true-anomaly (argument-perihelion orbit)))))

(defn ecliptical-to-equatorial [position obliquity]
  "translate ecliptical coordinates to equatorial"
  (let [[(, x y z) position]]
    (, x
       (- (* y (cosᵒ obliquity))
          (* z (sinᵒ obliquity)))
       (+ (* y (sinᵒ obliquity))
          (* z (cosᵒ obliquity))))))

(defn ra-decl [position]
  "translate ecliptical position into RA declination pair"
  (let [[(, x y z) position]]
    (, (normalize-angle (atan2ᵒ y x))
       (atan2ᵒ z 
               (math.sqrt (+ (pow x 2)
                             (pow y 2)))))))

(defn heliocentric-position [body d]
  "calculate heliocentric position of a body"
  (let [[planet-orbit (orbit body d)]]
    (heliocentric-location (distance-true-anomaly planet-orbit)
                           planet-orbit)))

(defn sun-loc [d]
  "calculate sun location"
  (let [[sun-orbit (orbit 'helios d)]
        [(, distance true-anomaly) (distance-true-anomaly sun-orbit)]
        [long (sun-long sun-orbit)]]
    (, (* distance (cosᵒ long))
       (* distance (sinᵒ long))
       0.0)))

(defn geocentric-position [body d]
  "geocentric position of a body"
  (list (map (fn [x] (+ (first x) (second x)))
             (zip (heliocentric-position body d)
                  (sun-loc d)))))

(defn ra-decl-of [body d]
  "calculate RA and declination of given body on given moment of time"
  (-> (cond [(= body 'helios) (sun-loc d)]
            [(= body 'selene) (heliocentric-position body d)]
            [true (geocentric-position body d)])      
      (ecliptical-to-equatorial (obliquity-of-ecliptic d))
      (ra-decl)))

(defn house-of [body d]
  "calculate zodiac house for given object"
  (ra-to-zodiac (normalize-angle (first (ra-decl-of body d)))))

(defn angle-between [body-1 body-2 d]
  "calculate angle between two bodies (RA)"
  (let [[(, ra1 decl1) (ra-decl-of body-1 d)]
        [(, ra2 decl2) (ra-decl-of body-2 d)]]
    (abs (- (normalize-angle ra1)
            (normalize-angle ra2)))))

(defn full-moon? [d]
  "is there more or less full moon at given time?"
  (<= 165.0
      (angle-between 'helios 'selene d)
      195.0))

(defn new-moon? [d]
  "is there more or less new moon at given time?"
  (<= (angle-between 'helios 'selene d) 15.0))
