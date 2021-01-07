CREATE TABLE area_info
(
    id        INT PRIMARY KEY,
    level     INT COMMENT '层级',
    code      VARCHAR(12) COMMENT '代码',
    name      VARCHAR(30) COMMENT '区划名称',
    parent_id INT NOT NULL COMMENT '上级区划id'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='地区表';
