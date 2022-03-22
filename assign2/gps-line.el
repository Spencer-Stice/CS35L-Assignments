(defun gps-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let* ((start (point-min))
	 (n (line-number-at-pos))
	 (pm (point-max))
	 (e (- (line-number-at-pos pm) 1)))
    (if (= start 1)
	(message "Line %d/%d" n e))))
