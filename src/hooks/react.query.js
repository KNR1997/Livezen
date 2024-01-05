import { useQuery } from "react-query";
import { fetchDistricts, fetchPlaceCategories, fetchPlaces, fetchProvices, fetchSubCategories } from "./useFetch";

export const getSubCategories = () => {
    return useQuery(
      [`fetchSubCategories`],
      () => fetchSubCategories(),
      {
        onError: (err) => {
          console.error("Error:", err);
        },
      }
    );
};

export const getProvinces = () => {
  return useQuery(
    [`fetchProvices`],
    () => fetchProvices(),
    {
      onError: (err) => {
        console.error("Error:", err);
      },
    }
  );
};

export const getDistricts = () => {
  return useQuery(
    [`fetchDistricts`],
    () => fetchDistricts(),
    {
      onError: (err) => {
        console.error("Error:", err);
      },
    }
  );
};

export const getPlaces = () => {
  return useQuery(
    [`fetchDistricts`],
    () => fetchPlaces(),
    {
      onError: (err) => {
        console.error("Error:", err);
      },
    }
  );
};

export const getPlaceCategories = () => {
  return useQuery(
    [`fetchDistricts`],
    () => fetchPlaceCategories(),
    {
      onError: (err) => {
        console.error("Error:", err);
      },
    }
  );
};