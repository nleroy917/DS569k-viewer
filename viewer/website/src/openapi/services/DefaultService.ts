/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SearchResponse } from '../models/SearchResponse';
import type { SimilarityQuery } from '../models/SimilarityQuery';
import type { TaxonomyInfo } from '../models/TaxonomyInfo';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DefaultService {
    /**
     * Taxonomy Info
     * Get available taxonomy classes and phyla for filtering.
     * @returns TaxonomyInfo Successful Response
     * @throws ApiError
     */
    public static taxonomyInfo(): CancelablePromise<TaxonomyInfo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/taxonomy-info',
        });
    }
    /**
     * Compute Similarity
     * @param requestBody
     * @returns SearchResponse Successful Response
     * @throws ApiError
     */
    public static computeSimilarity(
        requestBody: SimilarityQuery,
    ): CancelablePromise<SearchResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/search',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static readRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/',
        });
    }
}
