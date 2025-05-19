# Copyright 2020 The StackStorm Authors.
# Copyright 2019 Extreme Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import eventlet
import csv
from st2reactor.sensor.base import Sensor


class HelloSensor(Sensor):
    def __init__(self, sensor_service, config):
        super(HelloSensor, self).__init__(sensor_service=sensor_service, config=config)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._stop = False

    def setup(self):
        pass

    def run(self):
        while not self._stop:
            self._logger.debug("HelloSensor dispatching trigger...")
            count = self.sensor_service.get_value("hello_st2.count") or 0
            payload = {"greeting": "Yo, StackStorm!", "count": int(count) + 1}
            self.sensor_service.dispatch(trigger="hello_st2.event1", payload=payload)
            self.sensor_service.set_value("hello_st2.count", payload["count"])
            eventlet.sleep(10)
            try:
                last_id = 12345
                self.sensor_service.set_value(name='last_id', value=str(last_id))
                # kvp = self.sensor_service.get_value('last_id')
                kvp = self._datastore_service.get_value('last_id', local=True, decrypt=True, user='sensor_system')
                # CSV-Datei einlesen und als Liste von Dictionaries speichern
                # csv_datei = '/opt/stackstorm/packs/hello_st2/sensors/test.csv'
                # daten = []

                # with open(csv_datei, mode='r', encoding='utf-8') as file:
                #     reader = csv.DictReader(file)
                #     for zeile in reader:
                #         daten.append(zeile)
                payload = {"greeting": str(kvp), "count": int(count) + 1}
                self.sensor_service.dispatch(trigger="hello_st2.event1", payload=payload)
            except Exception as e:
                self._logger.error(f"Error occurred: {e}")
                payload = {"greeting": str(e), "count": int(count) + 1}
                self.sensor_service.dispatch(trigger="hello_st2.event1", payload=payload)
            

    def cleanup(self):
        self._stop = True

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
