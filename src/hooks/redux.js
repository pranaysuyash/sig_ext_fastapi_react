import { useDispatch, useSelector } from 'react-redux';

// Use these hooks throughout your app instead of plain useDispatch and useSelector
export const useAppDispatch = () => useDispatch();
export const useAppSelector = useSelector;