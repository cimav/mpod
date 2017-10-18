USE giancarlo_mpod;
DELETE FROM data_property;
DELETE FROM data_datafile_property;
INSERT INTO data_property (id, tag, description, tensor_dimensions, units, units_detail) VALUES (1, '_prop_magneto_striction', '_magneto_striction', 0, 'NULL', 'NULL');
INSERT INTO data_datafile_property (datafile_id, property_id) VALUES (1000369, 1);
UPDATE data_property SET name = ' prop magneto striction' WHERE tag = '_prop_magneto_striction';
UPDATE data_property SET units = '10^-12.s.m^-1' WHERE tag = '_prop_magneto_striction';
UPDATE data_property SET units_detail = 'pico second per inverse meter' WHERE tag = '_prop_magneto_striction';
COMMIT;
