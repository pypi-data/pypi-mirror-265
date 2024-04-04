import React, { useContext } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/oarepo_dashboard";
import { Button } from "semantic-ui-react";
import { withState } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";

const FacetsButtonGroupValueTogglerComponent = ({
  currentResultsState,
  currentQueryState,
  updateQueryState,
  facetName,
  trueButtonText,
  falseButtonText,
  keepFiltersOnUpdate,
  ...uiProps
}) => {
  const { initialQueryState } = useContext(SearchConfigurationContext);
  const currentFilter = currentQueryState.filters?.find(
    (f) => f[0] === facetName
  );
  const initialQueryFacets = initialQueryState.filters?.map((f) => f[0]);
  if (!currentFilter)
    console.error(
      "FacetsButtonGroup: Query does not contain this facet, make sure initial filters are set properly"
    );
  const currentStatus = currentFilter && JSON.parse(currentFilter?.[1]);
  const handeFacetStatusChange = (status) => {
    if (currentStatus === status) return;

    currentQueryState.filters = keepFiltersOnUpdate
      ? currentQueryState.filters.filter((element) => element[0] !== facetName)
      : [
          ...(currentQueryState?.filters
            ? currentQueryState.filters.filter((element) =>
                initialQueryFacets.includes(element[0])
              )
            : []),
        ];
    currentQueryState.filters = currentQueryState.filters.filter(
      (f) => f[0] !== facetName
    );

    currentQueryState.filters.push([facetName, status]);
    updateQueryState(currentQueryState);
  };
  return (
    <Button.Group size="mini" className="rel-mb-1" {...uiProps}>
      <Button
        onClick={() => handeFacetStatusChange(true)}
        className="request-search-filter"
        active={currentStatus}
      >
        {trueButtonText}
      </Button>
      <Button
        onClick={() => handeFacetStatusChange(false)}
        className="request-search-filter"
        active={!currentStatus}
      >
        {falseButtonText}
      </Button>
    </Button.Group>
  );
};

FacetsButtonGroupValueTogglerComponent.propTypes = {
  currentQueryState: PropTypes.object.isRequired,
  updateQueryState: PropTypes.func.isRequired,
  currentResultsState: PropTypes.object.isRequired,
  facetName: PropTypes.string.isRequired,
  trueButtonText: PropTypes.string,
  falseButtonText: PropTypes.string,
  keepFiltersOnUpdate: PropTypes.bool,
};
FacetsButtonGroupValueTogglerComponent.defaultProps = {
  trueButtonText: i18next.t("Open"),
  falseButtonText: i18next.t("Closed"),
  keepFiltersOnUpdate: true,
};
export const FacetsButtonGroupValueToggler = withState(
  FacetsButtonGroupValueTogglerComponent
);
