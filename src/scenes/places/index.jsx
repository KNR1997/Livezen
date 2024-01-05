import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataDistricts, mockDataPlaceCategories, mockDataPlaces, mockDataProvince, mockDataTeam, mockDataUsers } from "../../data/mockData";
import AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import LockOpenOutlinedIcon from "@mui/icons-material/LockOpenOutlined";
import SecurityOutlinedIcon from "@mui/icons-material/SecurityOutlined";
import Header from "../../components/Header";
import { getPlaces } from "../../hooks/react.query";

const Places = () => {
  const { data: places, isLoading, error } = getPlaces();
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const columns = [
    { field: "id", headerName: "ID" },
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "districts",
      headerName: "Districts",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "placeCategories",
      headerName: "Place Categories",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "subCategories",
      headerName: "Sub Categories",
      flex: 1,
      cellClassName: "name-column--cell",
    }
  ];

  let placesArray = places.map(place => ({
    id: place.id,
    name: place.name,
    districts: place.districts.map(district => district.name).join(', '),
    placeCategories: place.placeCategories.map(placeCategory => placeCategory.name).join(', '),
    subCategories: place.subCategories.map(subCategory => subCategory.name).join(', ')
    // other properties
  }));

  return (
    <Box m="20px">
      <Header title="PLACES" subtitle="Managing the Places" />
      {placesArray && (
        <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
        }}
      >
        <DataGrid checkboxSelection rows={placesArray} columns={columns} />
      </Box>
      )}
    </Box>
  );
};

export default Places;
