import axios from "axios";
import { BASE_URL } from "../../utils/config";

export const fetchSubCategories = async () => {
  const res = await axios({
    method: "get",
    url: `${BASE_URL}/subCategories/getPagedSubCategories`,
  });
  return res.data;
};

export const fetchProvices = async () => {
  const res = await axios({
    method: "get",
    url: `${BASE_URL}/province/getPagedProvinces`,
  });
  return res.data;
};

export const fetchDistricts = async () => {
  const res = await axios({
    method: "get",
    url: `${BASE_URL}/district/getPagedDistricts`,
  });
  return res.data;
};

export const fetchPlaces = async () => {
  const res = await axios({
    method: "get",
    url: `${BASE_URL}/PlaceNode/getPagedPlaceNodes`,
  });
  return res.data;
};

export const fetchPlaceCategories = async () => {
  const res = await axios({
    method: "get",
    url: `${BASE_URL}/placeCategory/getPagedPlaceCategories`,
  });
  return res.data;
};


