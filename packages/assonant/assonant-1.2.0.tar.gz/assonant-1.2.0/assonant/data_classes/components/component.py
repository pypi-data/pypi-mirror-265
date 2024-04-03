"""Assonant Component abstract class."""

from typing import Dict, List, Optional, Type, Union

import numpy as np

from ..assonant_data_class import AssonantDataClass
from ..data_handlers import Axis, DataField, DataHandler, TimeSeries
from ..exceptions import AssonantDataClassesError
from ..types import TransformationType


# TODO: Make this class abstract
class Component(AssonantDataClass):
    """Abstract class that creates the base common requirements to define an Assonant Component.

    Components are more generic definitions which may be composed by many subcomponents if more
    detailing in its composition is desired.
    """

    name: str
    subcomponents: Optional[List["Component"]] = []
    positions: Optional[List[Axis]] = []
    fields: Optional[Dict[str, DataHandler]] = {}

    def add_subcomponent(self, component: "Component"):
        """Add new subcomponent to component.

        Args:
            component (Component): Component object which will be add as
            subcomponent from called Component object.
        """
        self.subcomponents.append(component)

    def add_position(
        self,
        name: str,
        transformation_type: TransformationType,
        value: Union[int, float, str, List, Type[np.ndarray]],
        unit: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]] = None,
    ):
        """Add new positional field to component.

        Args:
            name (str): Axis name.
            transformation_type (TransformationType): Type of transformation done by axis.
            value (Union[int, float, str, List, Type[np.ndarray]]): Value related to axis
            collected data.
            unit (Optional[str], optional): Measurement unit related to value parameter.
            Defaults to None.
            extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]], optional): Dictionary
            containing any aditional metadata related to collected data. Defaults to None.
        """
        try:
            new_axis = Axis(
                name=name,
                transformation_type=transformation_type,
                value=DataField(
                    value=value,
                    unit=unit,
                    extra_metadata={} if extra_metadata is None else extra_metadata,
                ),
            )
        except Exception as e:
            raise AssonantDataClassesError(f"Failed to create Axis Data Handler for {self.name} Component.") from e
        try:
            self.positions.append(new_axis)
        except Exception as e:
            raise AssonantDataClassesError(f"Failed to add Axis to {self.name} Component positions list.") from e

    def add_timeseries_position(
        self,
        name: str,
        transformation_type: TransformationType,
        value: Union[int, float, str, List, Type[np.ndarray]],
        timestamps: Union[int, float, str, List, Type[np.ndarray]],
        unit: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]] = None,
        timestamps_unit: Optional[str] = None,
        timestamp_extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]] = None,
    ):
        """Add new positional field to component.

        Args:
            name (str): Axis name
            transformation_type (TransformationType): Transformation type of the Axis
            value (Union[int, float, str, List, Type[np.ndarray]]): Value related to
            axis collected data
            timestamps (Union[int, float, str, List, Type[np.ndarray]]): Timestamps
            related to data collected from the axis.
            unit (Optional[str], optional): Measurement unit related to value
            field. Defaults to None.
            extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]], optional): Dictionary
            containing extra metadata about value field. Defaults to None.
            tracked it as a TimeSeries. Defaults to None.
            timestamps_unit (Optional[str], optional): Measurement unit related to
            timestamp field. Defaults to None.
            timestamp_extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]], optional):
            Dictionary containing extra metadata about timestamps field. Defaults to None.
        """
        # Check if positions should be saved as a DataField or TimeSeries
        try:
            new_axis = Axis(
                name=name,
                transformation_type=transformation_type,
                value=TimeSeries(
                    value=DataField(
                        value=value,
                        unit=unit,
                        extra_metadata={} if extra_metadata is None else extra_metadata,
                    ),
                    timestamps=DataField(
                        value=timestamps,
                        unit=timestamps_unit,
                        extra_metadata={} if timestamp_extra_metadata is None else timestamp_extra_metadata,
                    ),
                ),
            )
        except Exception as e:
            raise AssonantDataClassesError(
                f"Failed to create Axis Data Handler with TimeSeries data for {self.name} " f"Component."
            ) from e
        try:
            self.positions.append(new_axis)
        except Exception as e:
            raise AssonantDataClassesError(
                f"Failed to add Axis with TimeSeries data to {self.name} Component positions" f" list."
            ) from e

    def add_field(
        self,
        name: str,
        value: Union[int, float, str, List, Type[np.ndarray]],
        unit: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]] = None,
    ):
        """Add new positional field to component that data was collected as a TimeSeries.

        Args:
            name (str): Field name.
            value (Union[int, float, str, List, Type[np.ndarray]]): Value related to field
            collected data.
            unit (Optional[str], optional): Measurement unit related to value parameter.
            Defaults to None.
            extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]], optional): Dictionary
            containing any aditional metadata related to collected data. Defaults to None.
        """
        try:
            new_field = DataField(
                value=value,
                unit=unit,
                extra_metadata={} if extra_metadata is None else extra_metadata,
            )
        except Exception as e:
            raise AssonantDataClassesError(f"Failed to create DataField Data Handler for {self.name} Component.") from e
        if name not in self.fields:
            self.fields[name] = new_field
        else:
            raise AssonantDataClassesError(f"Field name already exists on: {self.name} Component.")

    def add_timeseries_field(
        self,
        name: str,
        value: Union[int, float, str, List, Type[np.ndarray]],
        timestamps: Union[int, float, str, List, Type[np.ndarray]],
        unit: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]] = None,
        timestamps_unit: Optional[str] = None,
        timestamp_extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]] = None,
    ):
        """Add new positional field to component that data was collected as a TimeSeries.

        Args:
            name (str): Field name.
            value (Union[int, float, str, List, Type[np.ndarray]]): Value related to field
            collected data.
            timestamps (Union[int, float, str, List, Type[np.ndarray]]): Timestamps related to data collected
            from the field.
            unit (Optional[str], optional): Measurement unit related to value parameter.
            Defaults to None.
            extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]], optional): Dictionary
            containing any aditional metadata related to collected data. Defaults to None.
            timestamps_unit (Optional[str], optional): Measurement unit related to
            timestamp field. Defaults to None.
            timestamp_extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray]]]], optional):
            Dictionary containing extra metadata about timestamps field. Defaults to None.
        """
        try:
            new_field = TimeSeries(
                value=DataField(
                    value=value,
                    unit=unit,
                    extra_metadata={} if extra_metadata is None else extra_metadata,
                ),
                timestamps=DataField(
                    value=timestamps,
                    unit=timestamps_unit,
                    extra_metadata={} if timestamp_extra_metadata is None else timestamp_extra_metadata,
                ),
            )
        except Exception as e:
            raise AssonantDataClassesError(f"Failed to create DataField Data Handler for {self.name} Component.") from e
        if name not in self.fields:
            self.fields[name] = new_field
        else:
            raise AssonantDataClassesError(f"Field name already exists on: {self.name} Component.")
