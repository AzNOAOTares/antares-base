DROP TABLE IF EXISTS `AlertStatus`;

CREATE TABLE AlertStatus(
    id INT,
    alert_type CHAR(1), /* a=alert, r=replica, c=combo*/
    status CHAR(1), /* w=waiting, r=running, f=finished */
    stage INT,
    parent_id INT,
    original_alert_id INT,
    PRIMARY KEY (id)
    );
